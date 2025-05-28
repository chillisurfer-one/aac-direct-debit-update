import os
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path
import datetime
import json
from typing import Dict, List, Tuple, Any, Set
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from textwrap import dedent



AZURE_OPENAI_KEY="d006a38de36a4421bb75c0ccf44ca5ec"
AZURE_OPENAI_ENDPOINT="https://gpt-4-main.openai.azure.com/"
DEPLOYMENT_NAME="gpt-4o"
OPENAI_API_VERSION="2023-09-01-preview"
OPENAI_API_TYPE="azure"



# Hardcoded output directory for the report
#REPORT_OUTPUT_DIRECTORY = r"C:\Users\TAMANNAJANGID\Desktop\Natwest POC\Task-2/report3"

REPORT_OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "compliance-reports")
os.makedirs(REPORT_OUTPUT_DIRECTORY, exist_ok=True)

# # Define the report output directory
# REPORT_OUTPUT_DIRECTORY = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)), "compliance-reports"
# )

# os.makedirs(REPORT_OUTPUT_DIRECTORY, exist_ok=True)

# report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "terraform_compliance_report.md")
# with open(report_path, "w") as report_file:
#     report_file.write("# IaC Policy Compliance Report\n\n")
#     report_file.write("Validation completed successfully ✅\n")
# print(f"Report saved to: {report_path}")

# # Define the report output directory (absolute path based on script location)
# REPORT_OUTPUT_DIRECTORY = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)), "../compliance-reports"
# )
# # Ensure the directory exists
# os.makedirs(REPORT_OUTPUT_DIRECTORY, exist_ok=True)

# # Define the full report path within the repo
# report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "terraform_compliance_report.md")

# # Write the report content
# with open(report_path, "w") as report_file:
#     report_file.write("# IaC Policy Compliance Report\n\n")
#     report_file.write("Validation completed successfully ✅\n")

# print(f"Report saved to: {report_path}")

# end of update
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
        raise

def find_architecture_diagram(repo_dir):
    """Find the first PUML diagram in the repository"""
    puml_files = []
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.puml'):
                puml_files.append(os.path.join(root, file))

    if puml_files:
        return sorted(puml_files)[3]  # Return the path of the first one found
    return None

def find_infrastructure_folders(repo_dir):
    """Find all infrastructure folders containing Terraform files"""
    infra_dir = os.path.join(repo_dir, "infrastructure")
    
    # Check if infrastructure directory exists
    if not os.path.exists(infra_dir) or not os.path.isdir(infra_dir):
        # Try to find any folder containing Terraform files if "infrastructure" doesn't exist
        terraform_folders = []
        for root, dirs, files in os.walk(repo_dir):
            terraform_files = [f for f in files if f.endswith('.tf')]
            if 'main.tf' in terraform_files and 'variables.tf' in terraform_files and 'outputs.tf' in terraform_files:
                terraform_folders.append(root)
        return sorted(terraform_folders)

    terraform_folders = []
    for item in os.listdir(infra_dir):
        item_path = os.path.join(infra_dir, item)
        if os.path.isdir(item_path):
            # Check if folder contains all three Terraform files
            if all(os.path.exists(os.path.join(item_path, f)) for f in ["main.tf", "variables.tf", "outputs.tf"]):
                terraform_folders.append(item_path)
    return sorted(terraform_folders)

def load_file(path: str) -> str:
    """Load file content as string"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with a different encoding if UTF-8 fails
        with open(path, "r", encoding="latin-1") as f:
            return f.read()

def get_terraform_files_content(terraform_folder: str) -> Dict[str, str]:
    """Get content of all Terraform files in a folder"""
    file_contents = {}
    for filename in ["main.tf", "variables.tf", "outputs.tf"]:
        file_path = os.path.join(terraform_folder, filename)
        if os.path.exists(file_path):
            file_contents[filename] = load_file(file_path)
    return file_contents

def analyze_puml_with_llm(puml_code: str, llm, repo_dir: str) -> Dict[str, Any]:
    """
    Use LLM to parse the PlantUML code and identify key infrastructure components (e.g., VPCs, subnets, EC2 instances, load balancers, databases, gateways, etc.) ,connections, and module mappings.
    Returns a dictionary with components and connections and their module mappings
    """
    # First, identify all module folders to use as module names
    terraform_folders = find_infrastructure_folders(repo_dir)
    module_names = [os.path.basename(folder) for folder in terraform_folders]
    
    module_names_str = ", ".join([f"{i+1}. {name}" for i, name in enumerate(module_names)])
    
    prompt = dedent(f"""
    I need you to analyze this PlantUML diagram code and extract structured information from it.
    
    ```puml
    {puml_code}
    ```
    First, extract all the components defined in the diagram. Components are typically defined in node, component, 
    database, or similar blocks. Include any labels or names assigned to them.
    Next, extract all connections between components, noting the source, target, and any labels on the connections.
    
    ###Note- Client portal/CRM and Thought machine Vault core API are external components  so ignore them they are not part of any module.
    
    Finally, analyze the extracted components and logically map them to the following modules:
    {module_names_str}.Make sure you **Don't miss ** any module.
    
    Return the results in this exact JSON format:
    {{
        "components": [
            {{
                "name": "Component Name",
                "type": "component_type (node, database, etc.)",
                "module": "mapped_module_name"
            }},
            ...
        ],
        "connections": [
            {{
                "source": "Source Component Name",
                "target": "Target Component Name",
                "label": "Connection Label (if any)",
                "module": "mapped_module_name"
            }},
            ...
        ]
    }}
    
    The mapping for each component and connection should be your best assessment of which module would be responsible for that resource.
    The JSON should be valid and parseable, with all relevant information included.
    """)

    messages = [
        SystemMessage(content="You are a PlantUML analysis expert. You extract structured information from PlantUML diagrams and provide detailed JSON output."),
        HumanMessage(content=prompt),
    ]

    response = llm.invoke(messages)
    result_text = response.content
    
    # Extract JSON from the response
    import re
    json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        json_str = re.search(r'\{.*\}', result_text, re.DOTALL).group(0)
    
    # Parse the JSON
    analysis_result = json.loads(json_str)
    return analysis_result

def get_components_for_module(module_name: str, analysis_result: Dict[str, Any]) -> List[str]:
    """
    Extract the list of components that belong to a given module based on LLM analysis
    """
    components = []
    for component in analysis_result.get("components", []):
        if component.get("module") == module_name:
            components.append(component.get("name"))
    return components

def get_connections_for_module(module_name: str, analysis_result: Dict[str, Any]) -> List[str]:
    """
    Extract the list of connections that belong to a given module based on LLM analysis
    """
    connections = []
    for connection in analysis_result.get("connections", []):
        if connection.get("module") == module_name:
            source = connection.get("source")
            target = connection.get("target")
            label = connection.get("label", "")
            if label:
                connections.append(f"{source} -> {target}: {label}")
            else:
                connections.append(f"{source} -> {target}")
    return connections

def get_prompt_template_module_specific() -> PromptTemplate:
    template = dedent("""\
        Evaluate only the specific components and connections that belong to the "{module_name}" module as defined below:

        --- Architecture Diagram (PlantUML) ---
        {puml_code}

        --- Terraform Module: {module_name} ---

        # main.tf
        {main_tf}
        # variables.tf
        {variables_tf}
        # outputs.tf
        {outputs_tf}

        ### Components that should be part of module "{module_name}":
        {module_components}

        ### Connections that should be part of module "{module_name}":
        {module_connections}
        
        ### Evaluation Instructions for Module "{module_name}":
        Focus ONLY on the components and connections listed above that are specifically assigned to the "{module_name}" module and
        check for Check for standard architectural best practices (e.g., presence of public/private subnets, NAT gateways, availability zones, security layers).
        
        ## Task for Module "{module_name}":
        1. **Components Present in Diagram and Code:** List the components from the module-specific list above that have a corresponding resource or module in the Terraform code.
        2. **Components Present in Diagram Not in Code:** List the components from the module-specific list above that do NOT have a corresponding resource or module in the Terraform code.
        3. **Components Present in Code Not in Diagram:** List any resources or modules in the Terraform code that do not correspond to any component in the module-specific list above.
        4. **Connection Discrepancies:** Identify any connections from the module-specific list above that are not properly implemented in the Terraform code.
        5. **Label/Annotation Discrepancies:** Note any explicit labels or annotations on components or connections in the diagram that are not reflected in the code.

        Format your response as a markdown table with the following columns:
        | Category                                              | Details                                                         |
        |----------------------------------------------------------|----------------------------------------------------------------|
        | Components Present in PUML Diagram and Terraform Code    | (List of components, comma-separated)                           |
        | Components Present in PUML Diagram Not in Terraform Code | (List of components, comma-separated)                           |
        | Components Present in Terraform Code Not in PUML Diagram | (List of resources in code not shown in diagram)                |
        | Connection Discrepancies                                 | (Description of discrepancies, if any)                          |
        | Label/Annotation Discrepancies                           | (Description of discrepancies, if any)                          |

        Compliance for Module "{module_name}": (Yes/No - Based on whether all module-specific components and connections are accurately reflected in its code)

        If not compliant, please provide a section with specific remediation steps formatted as follows:
        
        #### Remediation Steps:
        
        1. **[Action Area 1]:**
           - Specific step 1
           - Specific step 2
        
        2. **[Action Area 2]:**
           - Specific step 1
           - Specific step 2
    """)
    return PromptTemplate.from_template(template)

def evaluate_terraform_module_tabular(puml_path: str, terraform_folder: str, llm, analysis_result: Dict[str, Any]) -> Tuple[str, bool]:
    """Evaluate a Terraform module against the architecture diagram and format output as a table."""
    puml_code = load_file(puml_path)
    module_name = os.path.basename(terraform_folder)

    terraform_files = get_terraform_files_content(terraform_folder)

    main_tf = terraform_files.get("main.tf", "# File not found")
    variables_tf = terraform_files.get("variables.tf", "# File not found")
    outputs_tf = terraform_files.get("outputs.tf", "# File not found")
    
    # Get components and connections specific to this module
    module_components = get_components_for_module(module_name, analysis_result)
    module_connections = get_connections_for_module(module_name, analysis_result)
    
    # Format the components and connections for the prompt
    formatted_components = "\n".join([f"- {comp}" for comp in module_components])
    formatted_connections = "\n".join([f"- {conn}" for conn in module_connections])

    prompt_template = get_prompt_template_module_specific()
    prompt = prompt_template.format(
        puml_code=puml_code,
        module_name=module_name,
        main_tf=main_tf,
        variables_tf=variables_tf,
        outputs_tf=outputs_tf,
        module_components=formatted_components,
        module_connections=formatted_connections
    )

    messages = [
        SystemMessage(content="You are a helpful assistant for Terraform and architecture compliance evaluation. You will output your analysis in a markdown table."),
        HumanMessage(content=prompt),
    ]

    response = llm.invoke(messages)
    result_text = response.content

    is_compliant = False  # Default to not compliant
    if result_text:
        lines = result_text.split('\n')
        for line in lines:
            if line.startswith("Compliance for Module"):
                compliance_status_text = line.split(":")[-1].strip().lower()
                if compliance_status_text == "yes":
                    is_compliant = True
                break

    return result_text, is_compliant

def evaluate_all_modules_tabular(puml_path: str, terraform_folders: List[str], repo_dir: str):
    """Evaluate all Terraform modules against the architecture diagram and generate tabular results."""
    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=OPENAI_API_VERSION,
        azure_deployment=DEPLOYMENT_NAME,
        temperature=0,  # Low temperature for more deterministic output
    )

    # First use LLM to extract components and connections from the PlantUML diagram
    puml_code = load_file(puml_path)
    
    # Pass repo_dir to analyze_puml_with_llm instead of using puml_code as path
    analysis_result = analyze_puml_with_llm(puml_code, llm, repo_dir)
    
    results = {}
    has_deviations = False

    if not terraform_folders:
        # Generate a report indicating no Terraform modules were found
        generate_summary_report_tabular({}, puml_path, analysis_result, no_modules_found=True)
        return False

    for terraform_folder in terraform_folders:
        folder_name = os.path.basename(terraform_folder)

        result_text, is_compliant = evaluate_terraform_module_tabular(
            puml_path, terraform_folder, llm, analysis_result
        )

        results[folder_name] = {
            "folder_path": terraform_folder,
            "result": result_text,
            "is_compliant": is_compliant
        }

        # If any module is not compliant, mark that we found a deviation
        if not is_compliant:
            has_deviations = True

    generate_summary_report_tabular(results, puml_path, analysis_result)
    return has_deviations

def extract_remediation_steps(result_text: str) -> str:
    """Extract remediation steps from result text if they exist"""
    if "#### Remediation Steps:" in result_text:
        remediation_section = result_text.split("#### Remediation Steps:")[1].strip()
        return "#### Remediation Steps:\n\n" + remediation_section
    return ""

def generate_summary_report_tabular(results: Dict[str, Dict[str, Any]], puml_path: str, 
                                   analysis_result: Dict[str, Any], no_modules_found: bool = False):
    """Generate a summary report of all evaluations in tabular format."""
    if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
        os.makedirs(REPORT_OUTPUT_DIRECTORY)

    puml_name = os.path.basename(puml_path).replace(".puml", "") if puml_path else "unknown"
    report_filename = "terraform_compliance_report.md"
    report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, report_filename)
    
    # Extract repo name from puml_path
    repo_dir = os.path.dirname(os.path.dirname(puml_path)) if puml_path else "unknown"
    repo_name = os.path.basename(repo_dir) if os.path.isdir(repo_dir) else "unknown"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Terraform Architecture Compliance Report\n\n")
        f.write(f"**Architecture Diagram**: `{os.path.basename(puml_path) if puml_path else 'Not found'}`  \n")
        f.write(f"**Date**: {datetime.datetime.now().strftime('%Y-%m-%d')}  \n")

        if no_modules_found:
            f.write("## Executive Summary\n\n")
            f.write("No Terraform modules were found in the repository.\n")
            f.write("Expected to find folders containing 'main.tf', 'variables.tf', and 'outputs.tf' files.\n\n")
            return
            
        # Count compliant and non-compliant modules
        compliant_count = sum(1 for data in results.values() if data.get("is_compliant", False))
        non_compliant_count = len(results) - compliant_count
        
        f.write("## Executive Summary\n\n")
        f.write(f"This report evaluates the compliance of Terraform modules against the architecture diagram. ")
        f.write(f"Of the {len(results)} modules evaluated, {compliant_count} ")
        f.write(f"{'are' if compliant_count != 1 else 'is'} compliant and {non_compliant_count} ")
        f.write(f"require{'s' if non_compliant_count == 1 else ''} remediation.\n\n")

        # Add module-component mapping section
        f.write("## Module to Component Mapping\n\n")
        f.write("The following table shows which components from the architecture diagram are mapped to each module:\n\n")
        f.write("| Module Name | Components |\n")
        f.write("|-------------|------------|\n")
        
        # Create module to component mapping
        module_to_components = {}
        for component in analysis_result.get("components", []):
            module = component.get("module")
            if module not in module_to_components:
                module_to_components[module] = []
            module_to_components[module].append(component.get("name"))
        
        for module_name in sorted(module_to_components.keys()):
            components = ", ".join(module_to_components[module_name])
            f.write(f"| {module_name} | {components} |\n")
        
        f.write("\n## Module Compliance Summary\n\n")
        f.write("| Module Name | Status | Action Required |\n")
        f.write("|-------------|--------|----------------|\n")

        # Sort results by module name for consistent ordering
        sorted_results = sorted(results.items(), key=lambda item: item[0])

        for module_name, data in sorted_results:
            is_compliant = data.get("is_compliant", False)
            compliance_status_text = "✅ COMPLIANT" if is_compliant else "❌ NON-COMPLIANT"
            action_required = "No" if is_compliant else "Yes"
            row = f"| {module_name} | {compliance_status_text} | {action_required} |\n"
            f.write(row)
            
        # Non-compliant modules section
        non_compliant_modules = {name: data for name, data in results.items() if not data.get("is_compliant", True)}
        if non_compliant_modules:
            f.write("\n## Non-Compliant Modules and Remediation Steps\n\n")
            
            for module_name, data in sorted(non_compliant_modules.items()):
                f.write(f"### {module_name}\n\n")
                
                # Extract table from the result
                result_text = data.get("result", "")
                table_lines = []
                capture = False
                
                for line in result_text.split('\n'):
                    if line.startswith('| Category'):
                        capture = True
                    if capture and line.strip() == '':
                        capture = False
                    if capture:
                        table_lines.append(line)
                
                # Write table
                if table_lines:
                    f.write('\n'.join(table_lines))
                    f.write('\n\n')
                    
                # Extract remediation steps section if it exists
                remediation_steps = extract_remediation_steps(result_text)
                if remediation_steps:
                    f.write(remediation_steps)
                else:
                    # Generate basic remediation steps if not provided by the LLM
                    f.write("#### Remediation Steps:\n\n")
                    f.write("1. **Review Architecture Diagram:**\n")
                    f.write("   - Carefully analyze the diagram components related to this module\n")
                    f.write("   - Compare with implemented Terraform code\n\n")
                    f.write("2. **Implement Missing Components/Connections:**\n")
                    f.write("   - Add the necessary Terraform resources\n")
                    f.write("   - Configure proper connections between components\n\n")
                
                f.write("\n---\n\n")

        # Compliant modules section (simplified)
        compliant_modules = {name: data for name, data in results.items() if data.get("is_compliant", False)}
        if compliant_modules:
            f.write("## Compliant Modules\n\n")
            
            for module_name, data in sorted(compliant_modules.items()):
                f.write(f"### {module_name}\n")
                f.write("✅ All diagram components and connections are correctly implemented in code.\n\n")

def main(github_repo_url):
    """Main function that handles the entire workflow"""
    repo_dir = None
    try:
        repo_dir = tempfile.mkdtemp()
        clone_repo(github_repo_url, repo_dir)

        # Find the first architecture diagram
        puml_path = find_architecture_diagram(repo_dir)
        if not puml_path:
            if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
                os.makedirs(REPORT_OUTPUT_DIRECTORY)
            error_report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "ERROR_REPORT_diagram_not_found.md")
            with open(error_report_path, "w") as erf:
                erf.write(f"# Evaluation Error\n\nFailed to find any PlantUML diagrams in the repository: {github_repo_url}\n")
                erf.write(f"Searched in: {repo_dir} (specifically 'architecture' folder or any .puml files)\n")
            return False, True  # Error occurred, but treat as no deviations

        # Find all infrastructure folders
        terraform_folders = find_infrastructure_folders(repo_dir)
        
        # Check if .puml file actually exists
        if not os.path.isfile(puml_path):
            if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
                os.makedirs(REPORT_OUTPUT_DIRECTORY)
            error_report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "ERROR_REPORT_invalid_puml.md")
            with open(error_report_path, "w") as erf:
                erf.write(f"# Evaluation Error\n\nThe PlantUML file found seems to be invalid: {puml_path}\n")
            return False, True

        # Evaluate all modules against the architecture diagram - pass repo_dir
        has_deviations = evaluate_all_modules_tabular(puml_path, terraform_folders, repo_dir)
        return True, has_deviations

    except Exception as e:
        if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
            os.makedirs(REPORT_OUTPUT_DIRECTORY)
        error_report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "CRITICAL_ERROR_REPORT.md")
        with open(error_report_path, "w") as erf:
            erf.write(f"# Critical Workflow Error\n\nAn unexpected error occurred during processing of repository {github_repo_url}:\n\n```\n{str(e)}\n```\n")
            import traceback
            erf.write("\n**Traceback:**\n```\n")
            traceback.print_exc(file=erf)
            erf.write("\n```\n")
        return False, True

    finally:
        if repo_dir and os.path.exists(repo_dir):
            try:
                shutil.rmtree(repo_dir)
            except Exception as e:
                pass

# if __name__ == "__main__":
#     # Replace with your GitHub repository URL
#     github_repo_url = "https://github.com/chillisurfer-one/aac-direct-debit-update"
#     success, has_deviations = main(github_repo_url)

#     if has_deviations:
#         # Exit with code 1 if deviations were found
#         sys.exit(1)
#     else:
#         # Exit with code 0 if no deviations were found
#         sys.exit(0)

if __name__ == "__main__":
    import os
    import sys

    # Replace with your GitHub repository URL
    github_repo_url = "https://github.com/chillisurfer-one/aac-direct-debit-update"
    success, has_deviations = main(github_repo_url)

    # --- Report Generation ---
    
    # REPORT_OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "compliance-reports")
    # os.makedirs(REPORT_OUTPUT_DIRECTORY, exist_ok=True)
    report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "validate_iac_deployment_architecture_report.md")
    with open(report_path, "w") as report_file:
        report_file.write("# IaC Policy Compliance Report\n\n")
        if has_deviations:
            report_file.write("❌ Deviations found in Terraform modules vs deployment architecture.\n")
        else:
            report_file.write("✅ Validation successful. All modules are compliant with the architecture.\n")
    print(f"Report saved to: {report_path}")
   # Print report content to GitHub Actions console
    print("\n--- Generated IaC Compliance Report ---")
    with open(report_path, "r") as report_file:
        print(report_file.read())
    print("--- End of Report ---\n")


    # # Define the report output directory
# REPORT_OUTPUT_DIRECTORY = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)), "compliance-reports"
# )
# os.makedirs(REPORT_OUTPUT_DIRECTORY, exist_ok=True)
# report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "terraform_compliance_report.md")
# with open(report_path, "w") as report_file:
#     report_file.write("# IaC Policy Compliance Report\n\n")
#     report_file.write("Validation completed successfully ✅\n")
# print(f"Report saved to: {report_path}")
    # with open(report_path, "r") as report_file:
    # print("\n--- Terraform Compliance Report ---\n")
    # print(report_file.read())
    # print("\n--- End of Report ---\n")

    
 


    # --- End Report Generation ---

    # Set exit code based on validation result
    sys.exit(1 if has_deviations else 0)
