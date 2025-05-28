import os
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path
import datetime
import json
import re
from typing import Dict, List, Tuple, Any, Set
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from textwrap import dedent
import stat
import re

# Azure OpenAI Configuration
AZURE_OPENAI_KEY = "d006a38de36a4421bb75c0ccf44ca5ec" # Replace with your actual key or use environment variables
AZURE_OPENAI_ENDPOINT = "https://gpt-4-main.openai.azure.com/" # Replace with your actual endpoint
DEPLOYMENT_NAME = "gpt-4o"
OPENAI_API_VERSION = "2023-09-01-preview"
OPENAI_API_TYPE = "azure"

# Hardcoded output directory for the report
#REPORT_OUTPUT_DIRECTORY = r"C:\Users\TAMANNAJANGID\Desktop\Natwest POC\Task-4\result" # Ensure this path is correct

# updated
REPORT_OUTPUT_DIRECTORY = os.path.join("aac-direct-debit-update", "compliance-reports")

def clone_repo(repo_url, target_dir=None):
    """Clone a GitHub repository to a specified directory or a temporary directory"""
    if target_dir is None:
        target_dir = tempfile.mkdtemp()
    try:
        subprocess.run(
            ["git", "clone", repo_url, target_dir],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return target_dir
    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to clone repository: {e.stderr.decode() if e.stderr else e.stdout.decode()}")
    except FileNotFoundError:
        raise Exception("Git command not found. Ensure Git is installed and in your PATH.")

def find_all_control_folders(repo_dir):
    """Find all control folders (INFRA-00X-control and SEC-00X-control)"""
    controls_dir = os.path.join(repo_dir, "controls")
    
    if not os.path.exists(controls_dir) or not os.path.isdir(controls_dir):
        return [], []
    
    infra_controls = []
    sec_controls = []
    
    for item in os.listdir(controls_dir):
        item_path = os.path.join(controls_dir, item)
        if os.path.isdir(item_path) and item.endswith("-control"):
            if item.startswith("INFRA-"):
                infra_controls.append(item_path)
            elif item.startswith("SEC-"):
                sec_controls.append(item_path)
    
    return sorted(infra_controls), sorted(sec_controls)

def find_infrastructure_modules(repo_dir):
    """Find all Terraform modules in the infrastructure folder"""
    infra_dir = os.path.join(repo_dir, "infrastructure")
    
    if not os.path.exists(infra_dir) or not os.path.isdir(infra_dir):
        return []
    
    terraform_modules = []
    for item in os.listdir(infra_dir):
        item_path = os.path.join(infra_dir, item)
        if os.path.isdir(item_path):
            required_files = ["main.tf", "variables.tf", "outputs.tf"]
            if all(os.path.exists(os.path.join(item_path, f)) for f in required_files):
                terraform_modules.append(item_path)
    return sorted(terraform_modules)

def load_file(path: str) -> str:
    """Load file content as string"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            return f"# Error reading file (latin-1): {path}"
    except Exception as e:
        return f"# File not found or error reading: {path}"

def get_terraform_module_content(module_folder: str) -> Dict[str, str]:
    """Get content of all Terraform files in a module folder"""
    file_contents = {}
    for filename in ["main.tf", "variables.tf", "outputs.tf"]:
        file_path = os.path.join(module_folder, filename)
        file_contents[filename] = load_file(file_path)
    return file_contents

def get_control_rego_json_files(control_folder_path: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Get .rego and .json files from control folder separately"""
    rego_files = {}
    json_files = {}
    
    if not os.path.exists(control_folder_path):
        return rego_files, json_files
    
    for root, dirs, files in os.walk(control_folder_path):
        # Skip .git directories
        if ".git" in dirs:
            dirs.remove(".git")
            
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, control_folder_path)
            
            if file.endswith('.rego'):
                rego_files[relative_path] = load_file(file_path)
            elif file.endswith('.json'):
                json_files[relative_path] = load_file(file_path)
    
    return rego_files, json_files

def create_control_dictionary(infra_controls: List[str], sec_controls: List[str], repo_dir: str) -> Dict[str, str]:
    """Create a dictionary with control ID and description from Policy and Purpose columns in controls_as_code_policy_index.md"""
    control_dict = {}
    all_controls = infra_controls + sec_controls
    
    # Path to the main controls policy index file
    policy_index_path = os.path.join(repo_dir, "controls", "controls_as_code_policy_index.md")
    
    # Check if the policy index file exists
    if not os.path.exists(policy_index_path):
        # Fallback: create empty entries for each control
        for control_folder in all_controls:
            control_id = os.path.basename(control_folder)
            control_dict[control_id] = "No description available - policy index file not found"
        return control_dict
    
    try:
        # Load the policy index file content
        policy_content = load_file(policy_index_path)
        
        # Updated pattern to match both INFRA and SEC controls
        pattern = r'((?:INFRA|SEC)-\d+-control)\*\*([^*]+)\*\*([^*\n]+?)(?=(?:INFRA|SEC)-|\Z)'
        
        matches = re.findall(pattern, policy_content, re.DOTALL)
        
        if matches:
            for match in matches:
                control_id = match[0].strip()
                policy_text = match[1].strip()
                purpose_text = match[2].strip()
                
                # Clean up the text (remove extra asterisks, clean whitespace)
                policy_text = re.sub(r'\*+', '', policy_text).strip()
                purpose_text = re.sub(r'\*+', '', purpose_text).strip()
                
                # Combine policy and purpose as description
                description_parts = []
                if policy_text and policy_text not in ['', '-', 'N/A', 'TBD']:
                    description_parts.append(f"**Policy**: {policy_text}")
                if purpose_text and purpose_text not in ['', '-', 'N/A', 'TBD']:
                    description_parts.append(f"**Purpose**: {purpose_text}")
                
                if description_parts:
                    combined_description = '\n\n'.join(description_parts)
                    control_dict[control_id] = combined_description
                else:
                    control_dict[control_id] = "No policy or purpose information available"
        
        else:
            # Split content and look for control patterns
            lines = policy_content.split('\n')
            
            for line in lines:
                line = line.strip()
                if 'INFRA-' in line or 'SEC-' in line:
                    # Try to extract control IDs and surrounding text
                    control_matches = re.finditer(r'(?:INFRA|SEC)-\d+-control', line, re.IGNORECASE)
                    
                    for control_match in control_matches:
                        control_id = control_match.group(0)
                        
                        # Get text after the control ID
                        remaining_text = line[control_match.end():].strip()
                        
                        # Remove leading/trailing asterisks and clean up
                        remaining_text = re.sub(r'^\*+|\*+$', '', remaining_text).strip()
                        
                        if remaining_text:
                            control_dict[control_id] = f"**Description**: {remaining_text}"
                        else:
                            control_dict[control_id] = "Description extracted but empty"
        
        # Ensure all found controls have entries (fallback for missing ones)
        for control_folder in all_controls:
            control_id = os.path.basename(control_folder)
            if control_id not in control_dict:
                control_dict[control_id] = "Description not found in policy index file"
        
    except Exception as e:
        import traceback
        # Fallback: create error entries for each control
        for control_folder in all_controls:
            control_id = os.path.basename(control_folder)
            control_dict[control_id] = f"Error reading policy index file: {str(e)}"
    
    return control_dict

def analyze_control_mapping(module_path: str, module_content: Dict[str, str],
                           control_dict: Dict[str, str], all_controls: List[str],
                           repo_dir: str, llm, control_type: str = "ALL") -> Dict[str, Any]:
    """Analyze which controls (INFRA/SEC) a Terraform module implements"""
    module_name = os.path.basename(module_path)
    
    # Filter controls based on type if specified
    if control_type == "INFRA":
        filtered_controls = [c for c in all_controls if "INFRA-" in os.path.basename(c)]
        control_type_text = "INFRA"
    elif control_type == "SEC":
        filtered_controls = [c for c in all_controls if "SEC-" in os.path.basename(c)]
        control_type_text = "SEC"
    else:
        filtered_controls = all_controls
        control_type_text = "INFRA and SEC"
    
    # Format control dictionary for prompt
    control_descriptions = ""
    for control_folder in filtered_controls:
        control_id = os.path.basename(control_folder)
        description = control_dict.get(control_id, "No description available")
        control_descriptions += f"\n### {control_id}\n{description}\n"
    
    # Get .rego and .json files from all control folders separately
    all_rego_files_text = ""
    all_json_files_text = ""
    
    for control_folder in filtered_controls:
        control_id = os.path.basename(control_folder)
        rego_files, json_files = get_control_rego_json_files(control_folder)
        
        if rego_files:
            all_rego_files_text += f"\n## {control_id} - Rego Policy Rules\n"
            for file_path, content in rego_files.items():
                all_rego_files_text += f"\n### {file_path}\n```rego\n{content[:2000]}{'...' if len(content) > 2000 else ''}\n```\n"
        
        if json_files:
            all_json_files_text += f"\n## {control_id} - JSON Configuration\n"
            for file_path, content in json_files.items():
                all_json_files_text += f"\n### {file_path}\n```json\n{content[:2000]}{'...' if len(content) > 2000 else ''}\n```\n"

    prompt = dedent(f"""
    Analyze the Terraform module code against {control_type_text} control policies.

    ## Terraform Module: {module_name}

    ### main.tf
    ```terraform
    {module_content.get('main.tf', '# File not found')}
    ```
    
    ### variables.tf
    ```terraform
    {module_content.get('variables.tf', '# File not found')}
    ```
    
    ### outputs.tf
    ```terraform
    {module_content.get('outputs.tf', '# File not found')}
    ```

    ## {control_type_text} Control Policies:
    {control_descriptions}

    ## Rego Policy Rules:
    {all_rego_files_text}

    ## JSON Configuration Files:
    {all_json_files_text}

    ## Instructions:
    Compare the Terraform module code with each {control_type_text} control policy. Only map a control if the module code explicitly implements the policy requirements.

    Check for:
    - Resource configurations matching policy requirements
    - Security settings as specified in policies
    - Configuration values matching policy specifications
    - Required attributes and settings

    ## Response Format (JSON only):
    ```json
    {{
        "module_name": "{module_name}",
        "control_type": "{control_type_text}",
        "implemented_controls": [
            {{
                "control_id": "INFRA-XXX-control or SEC-XXX-control",
                "reason": "Specific code reference showing implementation"
            }}
        ]
    }}
    ```

    Only include controls with clear implementation evidence in the provided code.
    """)

    messages = [
        SystemMessage(content=f"Analyze Terraform code against {control_type_text} control policies. Base analysis only on provided code. Respond in JSON format only."),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        result_text = response.content
        
        json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
        if not json_match:
            json_match = re.search(r'(\{[\s\S]*\})', result_text)

        if json_match:
            json_str = json_match.group(1)
            analysis_result = json.loads(json_str)
            return analysis_result
        else:
            raise Exception("No JSON found in LLM response")
        
    except Exception as e:
        return {"module_name": module_name, "control_type": control_type_text, "implemented_controls": [], "error": str(e)}

def analyze_policy_deviations(module_name: str, module_content: Dict[str, str],
                            control_id: str, rego_files: Dict[str, str], 
                            json_files: Dict[str, str], llm) -> Dict[str, Any]:
    """Analyze deviations of a module against a specific control policy"""
    
    # Format .rego files for prompt
    rego_files_text = ""
    for file_path, content in rego_files.items():
        rego_files_text += f"\n### {file_path}\n```rego\n{content}\n```\n"

    # Format .json files for prompt
    json_files_text = ""
    for file_path, content in json_files.items():
        json_files_text += f"\n### {file_path}\n```json\n{content}\n```\n"

    prompt = dedent(f"""
    Analyze Terraform module compliance against control policy files.

    ## Module: {module_name}
    ## Control: {control_id}

    ### Terraform Code:
    #### main.tf
    ```terraform
    {module_content.get('main.tf', '# File not found')}
    ```
    
    #### variables.tf
    ```terraform
    {module_content.get('variables.tf', '# File not found')}
    ```
    
    #### outputs.tf
    ```terraform
    {module_content.get('outputs.tf', '# File not found')}
    ```

    ### Rego Policy Rules:
    {rego_files_text}

    ### JSON Configuration:
    {json_files_text}

    ## Instructions:
    Compare the Terraform code against the rego rules and json configuration. Identify deviations where the code does not match policy requirements.

    Check for:
    - Missing required configurations
    - Incorrect configuration values
    - Missing required resources or attributes
    - Non-compliance with policy rules

    ## Response Format (JSON only):
    ```json
    {{
        "module_name": "{module_name}",
        "control_id": "{control_id}",
        "compliance_status": "Compliant|Non-Compliant",
        "deviations": [
            {{
                "deviation_description": "Specific deviation with code reference",
                "suggestion": "Required code change",
                "policy_reference": "Reference to rego rule or json spec"
            }}
        ]
    }}
    ```

    Use "Compliant" if code meets all policy requirements. Use "Non-Compliant" if any deviations found.
    If compliant, return empty deviations array.
    """)

    messages = [
        SystemMessage(content="Analyze compliance based only on provided code and policy files. Respond in JSON format only."),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        result_text = response.content
        
        json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
        if not json_match:
            json_match = re.search(r'(\{[\s\S]*\})', result_text)

        if json_match:
            json_str = json_match.group(1)
            analysis_result = json.loads(json_str)
            return analysis_result
        else:
            return {
                "module_name": module_name, 
                "control_id": control_id,
                "compliance_status": "Error",
                "deviations": [{"deviation_description": "Failed to parse LLM response", "suggestion": "Manual review required"}],
                "error": "JSON parsing failed"
            }
        
    except Exception as e:
        return {
            "module_name": module_name, 
            "control_id": control_id,
            "compliance_status": "Error",
            "deviations": [{"deviation_description": f"Analysis error: {str(e)}", "suggestion": "Manual review required"}],
            "error": str(e)
        }

def check_for_deviations(deviation_results: List[Dict[str, Any]]) -> bool:
    """Check if any deviations were found in the analysis results"""
    has_deviations = False
    
    for result in deviation_results:
        compliance_status = result.get('compliance_status', 'Unknown')
        deviations = result.get('deviations', [])
        
        # Check if the result indicates non-compliance
        if compliance_status == "Non-Compliant":
            has_deviations = True
            break
            
        # Check if there are actual deviations listed
        if deviations and len(deviations) > 0:
            # Filter out empty deviations or generic error messages
            real_deviations = [
                dev for dev in deviations 
                if dev.get('deviation_description', '').strip() 
                and dev.get('deviation_description', '') not in ['No deviations found', 'N/A', '']
            ]
            if real_deviations:
                has_deviations = True
                break
    
    return has_deviations

def generate_report(mapping_results: List[Dict[str, Any]],
                   deviation_results: List[Dict[str, Any]],
                   repo_name: str):
    """Generate comprehensive control mapping and deviation report"""
    if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
        os.makedirs(REPORT_OUTPUT_DIRECTORY)
    
    report_filename = f"{repo_name}_control_analysis.md"
    report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, report_filename)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# IaC - Control Policy Deviation Report\n\n")
        f.write(f"**Analysis Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Control Mapping Section - removed control type column
        f.write("## 1. IaC Module and Control Policy Mapping\n\n")
        if mapping_results:
            f.write("| Iac Module     | Control ID | Implementation Evidence |\n")
            f.write("|----------------|------------|-------------------------|\n")
            
            for result in mapping_results:
                module_name = result.get('module_name', 'Unknown')
                implemented_controls = result.get('implemented_controls', [])
                error = result.get('error')
                
                if error:
                    f.write(f"| {module_name} | Analysis Failed | {error[:200]}... |\n")
                elif implemented_controls:
                    for i, control in enumerate(implemented_controls):
                        control_id = control.get('control_id', 'Unknown')
                        reason = control.get('reason', 'No reason provided').replace('\n', ' ').replace('|', '\\|').strip()
                        if len(reason) > 300: 
                            reason = reason[:297] + "..."
                        
                        display_name = module_name if i == 0 else ""
                        f.write(f"| {display_name} | {control_id} | {reason} |\n")
                else:
                    f.write(f"| {module_name} | No policies mapped | N/A |\n")
        else:
            f.write("*No mapping analysis results available.*\n")
        
        # Deviation Analysis Section - removed control type column
        f.write("\n## 2. Control Policy Deviation Analysis\n\n")
        if deviation_results:
            f.write("| Iac Module | Control ID | Compliance Status         | Deviation | Suggestion |\n")
            f.write("|------------|------------|---------------------------|-----------|------------|\n")
            
            for result in deviation_results:
                module_name = result.get('module_name', 'Unknown')
                control_id = result.get('control_id', 'Unknown')
                status = result.get('compliance_status', 'Unknown')
                deviations = result.get('deviations', [])
                
                # Convert status to symbols
                if status == "Compliant":
                    status_symbol = "Complaint✅"
                elif status == "Non-Compliant":
                    status_symbol = "Non-Compliant❌"
                else:
                    status_symbol = "❓"
                
                if not deviations or status == "Compliant":
                    f.write(f"| {module_name} | {control_id} | {status_symbol} | No deviations found | N/A |\n")
                else:
                    for i, dev in enumerate(deviations):
                        desc = dev.get('deviation_description', 'N/A').replace('\n', ' ').replace('|', '\\|')[:200]
                        sugg = dev.get('suggestion', 'N/A').replace('\n', ' ').replace('|', '\\|')[:200]
                        
                        display_name = module_name if i == 0 else ""
                        display_control = control_id if i == 0 else ""
                        display_status = status_symbol if i == 0 else ""
                        
                        f.write(f"| {display_name} | {display_control} | {display_status} | {desc} | {sugg} |\n")
        else:
            f.write("*No deviation analysis performed.*\n")


def remove_readonly(func, path, _):
    """Clear the readonly bit and reattempt the removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def safe_cleanup_temp_dir(temp_dir):
    """Safely clean up temporary directory, handling Windows readonly files"""
    if not temp_dir or not os.path.exists(temp_dir):
        return
    
    try:
        # First attempt: normal removal
        shutil.rmtree(temp_dir)
    except PermissionError:
        try:
            # Second attempt: handle readonly files (common with Git on Windows)
            shutil.rmtree(temp_dir, onerror=remove_readonly)
        except Exception as cleanup_error:
            pass  # Silent cleanup failure

def main(github_repo_url):
    """Main function for control analysis workflow"""
    repo_dir = None
    repo_name = os.path.basename(github_repo_url.rstrip('/').replace('.git', ''))

    try:
        repo_dir = tempfile.mkdtemp() 
        cloned_repo_path = os.path.join(repo_dir, "cloned_repo") 
        clone_repo(github_repo_url, cloned_repo_path)
        
        # Find INFRA and SEC controls and modules
        infra_controls, sec_controls = find_all_control_folders(cloned_repo_path)
        terraform_modules = find_infrastructure_modules(cloned_repo_path)
        
        if not terraform_modules:
            generate_report([], [], repo_name)
            return True, False  # Success but no modules to analyze
        
        if not infra_controls and not sec_controls:
            generate_report([], [], repo_name)
            return True, False  # Success but no controls to analyze
        
        # Create control dictionary using the policy index file
        control_dict = create_control_dictionary(infra_controls, sec_controls, cloned_repo_path)
        
        # Initialize LLM
        llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            api_version=OPENAI_API_VERSION,
            azure_deployment=DEPLOYMENT_NAME,
            temperature=0.0,
            max_retries=3,
        )
        
        mapping_results = []
        deviation_results = []
        all_controls = infra_controls + sec_controls
        
        for module_path in terraform_modules:
            module_name = os.path.basename(module_path)
            
            module_content = get_terraform_module_content(module_path)
            
            # Step 1: Control Mapping for both INFRA and SEC controls
            mapping_result = analyze_control_mapping(
                module_path, module_content, control_dict, all_controls, cloned_repo_path, llm, "ALL"
            )
            mapping_results.append(mapping_result)
            
            # Step 2: Deviation Analysis for mapped controls  
            implemented_controls = mapping_result.get('implemented_controls', [])
            if implemented_controls and not mapping_result.get('error'):
                for control_map in implemented_controls:
                    control_id = control_map.get('control_id')
                    if not control_id:
                        continue
                    
                    # Find control folder path
                    control_folder = None
                    for folder in all_controls:
                        if os.path.basename(folder) == control_id:
                            control_folder = folder
                            break
                    
                    if not control_folder:
                        continue
                    
                    # Get .rego and .json files from control folder separately
                    rego_files, json_files = get_control_rego_json_files(control_folder)
                    
                    deviation_result = analyze_policy_deviations(
                        module_name, module_content, control_id, rego_files, json_files, llm
                    )
                    deviation_results.append(deviation_result)
        
        # Generate final report
        generate_report(mapping_results, deviation_results, repo_name)
        
        # Check for deviations
        has_deviations = check_for_deviations(deviation_results)
        
        return True, has_deviations
        
    except Exception as e:
        # Handle errors and create error report
        if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
            os.makedirs(REPORT_OUTPUT_DIRECTORY)
        error_report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "CRITICAL_ERROR_REPORT.md")
        with open(error_report_path, "w") as erf:
            erf.write(f"# Critical Workflow Error\n\nAn unexpected error occurred during processing of repository {github_repo_url}:\n\n```\n{str(e)}\n```\n")
            import traceback
            erf.write("\n**Traceback:**\n```\n")
            traceback.print_exc(file=erf)
            erf.write("\n```\n")
        return False, False  # Error occurred, treat as no deviations since we can't determine otherwise
        
    finally:
        # Clean up temporary directory with improved error handling
        if repo_dir:
            safe_cleanup_temp_dir(repo_dir)

if __name__ == "__main__":
    repo_url = "https://github.com/chillisurfer-one/aac-direct-debit-update"

    if not repo_url:
        sys.exit(1)
    else:
        success, has_deviations = main(repo_url)

        if has_deviations:
            #Exit with code 1 if deviations were found
            sys.exit(1)
        else:
            #Exit with code 0 if no deviations were found
            sys.exit(0)
