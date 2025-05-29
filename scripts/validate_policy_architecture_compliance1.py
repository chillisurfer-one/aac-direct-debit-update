import os
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import datetime
import json
import time

# Load environment variables from .env
load_dotenv()

# AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
# AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
# OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
# OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE")

AZURE_OPENAI_KEY="d006a38de36a4421bb75c0ccf44ca5ec"
AZURE_OPENAI_ENDPOINT="https://gpt-4-main.openai.azure.com/"
DEPLOYMENT_NAME="gpt-4o"
OPENAI_API_VERSION="2023-09-01-preview"
OPENAI_API_TYPE="azure"

# Define the report output directory
REPORT_OUTPUT_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "compliance-reports")


# Hardcoded output directory for the report
#REPORT_OUTPUT_DIRECTORY = r"C:\Users\TAMANNAJANGID\Desktop\Natwest POC\Task-1" # Use your actual path

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

def find_architecture_diagrams(repo_dir):
    """Find all PUML diagrams in the architecture directory"""
    architecture_dir = os.path.join(repo_dir, "architecture")

    if not os.path.exists(architecture_dir):
        for root, dirs, files in os.walk(repo_dir):
            puml_files = [f for f in files if f.endswith('.puml')]
            if puml_files:
                return [os.path.join(root, f) for f in puml_files]
        return []

    puml_files = []
    for root, dirs, files in os.walk(architecture_dir):
        for file in files:
            if file.endswith('.puml'):
                puml_files.append(os.path.join(root, file))

    return sorted(puml_files)

def find_policies_dir(repo_dir):
    """Find the policies directory in the repository"""
    policies_dir = os.path.join(repo_dir, "policies")

    if os.path.exists(policies_dir) and os.path.isdir(policies_dir):
        return policies_dir

    for root, dirs, files in os.walk(repo_dir):
        for dir_name in dirs:
            if dir_name.lower() == "policies":
                return os.path.join(root, dir_name)

    for root, dirs, files in os.walk(repo_dir):
        policy_files = [f for f in files if f.endswith('.rego')]
        if policy_files:
            return root

    return None

def load_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def get_policy_folders(policies_dir: str) -> list:
    """Get all policy folders that follow the pattern ARC-POLICY-XXX-control"""
    policy_folders = []
    if not policies_dir or not os.path.exists(policies_dir): # Added check for policies_dir
        return []
    for item in os.listdir(policies_dir):
        item_path = os.path.join(policies_dir, item)
        if os.path.isdir(item_path) and item.startswith("ARC-POLICY-") and item.endswith("-control"):
            policy_folders.append(item_path)
    return sorted(policy_folders)

def get_policy_index(policies_dir: str) -> dict:
    """Load and parse the policy index markdown file into ARC-POLICY IDs, combining description + intent."""
    if not policies_dir or not os.path.exists(policies_dir): # Added check
        return {}

    index_path = os.path.join(policies_dir, "aac_architecture_policy_index.md")
    if not os.path.exists(index_path):
        alternate_names = ["policy_index.md", "architecture_policy_index.md", "index.md"]
        for name in alternate_names:
            alt_path = os.path.join(policies_dir, name)
            if os.path.exists(alt_path):
                index_path = alt_path
                break
        else:
            return {}


    index_content = load_file(index_path)
    policy_index = {}

    lines = index_content.strip().split('\n')
    for line in lines:
        if line.startswith('|') and ('AAC-' in line or 'ARC-POLICY-' in line):
            parts = [part.strip() for part in line.strip().split('|')]
            if len(parts) >= 4: # Ensure enough parts for ID, description, and intent
                id_raw = parts[1].replace('**', '').strip()
                policy_desc = parts[2].strip()
                intent_reason = parts[3].strip() if len(parts) > 3 else ""

                full_description = f"{policy_desc}"
                if intent_reason:
                    full_description += f" — {intent_reason}"

                if id_raw.startswith('AAC-'):
                    try:
                        policy_num = id_raw.split('-')[-1]
                        arc_id = f"ARC-POLICY-{policy_num}"
                    except IndexError:
                        continue # Skip this entry
                else:
                    arc_id = id_raw

                policy_index[arc_id] = full_description
    return policy_index

def get_prompt_template() -> PromptTemplate:
    template = """You are a knowledgeable architecture compliance expert.

You will analyze the following components to determine if the UML diagram adheres to the provided OPA policy:

--- UML Diagram (PlantUML) ---
{puml_code}

--- Policy (Rego) ---
{policy_code}

--- Policy Input JSON ---
{input_json}

--- Expected Policy Output JSON ---
{output_json}

Policy ID: {policy_id}
Policy Description: {policy_description}

Task:
1. Evaluate whether the UML diagram complies with the policy.
2. For non-compliance, list each deviation clearly with:
    - What is wrong
    - Why it violates the policy (referencing the policy logic)
3. Suggest concrete, actionable fixes for each deviation.
4. Provide your conclusion on compliance as "Yes" or "No".

Respond in the following format:

Compliance: Yes / No

Deviations:
- 1: Explanation and reason.
- 2: Explanation and reason.
... (If no deviations, state "None")

Suggestions:
- 1: How to fix deviation 1.
- 2: How to fix deviation 2.
... (If no deviations, state "None")

Please be concise but thorough, and ensure clarity for a software architecture reviewer.
"""
    return PromptTemplate.from_template(template)

def evaluate_policy(puml_path: str, policy_folder_path: str, llm, policy_id: str = "", policy_description: str = ""):
    puml_code = load_file(puml_path)

    policy_file = os.path.join(policy_folder_path, "policy.rego")
    input_file = os.path.join(policy_folder_path, "test_input.json")
    output_file = os.path.join(policy_folder_path, "expected_result.json")

    if not all(os.path.exists(f) for f in [policy_file, input_file, output_file]):
        return None, False # Ensure two values are returned

    policy_code = load_file(policy_file)
    input_json_content = load_file(input_file)
    output_json_content = load_file(output_file)

    prompt_template = get_prompt_template()
    prompt = prompt_template.format(
        puml_code=puml_code,
        policy_code=policy_code,
        input_json=input_json_content,
        output_json=output_json_content,
        policy_id=policy_id,
        policy_description=policy_description,
    )

    messages = [
        SystemMessage(content="You are a helpful assistant for policy compliance evaluation."),
        HumanMessage(content=prompt),
    ]

    response = llm.invoke(messages)
    result_text = response.content

    is_compliant = False # Default to not compliant
    has_deviations = True # Default to having deviations

    if result_text:
        lines = result_text.split('\n')
        for line in lines:
            if line.startswith("Compliance:"):
                compliance_status_text = line.replace("Compliance:", "").strip().lower()
                if compliance_status_text == "yes":
                    is_compliant = True
                break
        if "Deviations:" in result_text:
            deviations_section = result_text.split("Deviations:")[1].split("Suggestions:")[0]
            # Check if "None" is present or if there are no lines starting with "- ["
            deviation_lines = [line.strip() for line in deviations_section.strip().split('\n') if line.strip()]
            if not deviation_lines or (len(deviation_lines) == 1 and deviation_lines[0].lower() == "none"):
                has_deviations = False
            elif not any(line.startswith("- [") for line in deviation_lines): # if no lines start with "- ["
                has_deviations = False


        else: # No "Deviations:" section implies no deviations by the prompt's structure
            has_deviations = False

    final_is_compliant = is_compliant and not has_deviations

    return result_text, final_is_compliant


def evaluate_all_policies(puml_path: str, policies_dir: str):
    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version=OPENAI_API_VERSION,
        azure_deployment=DEPLOYMENT_NAME,
        temperature=0.2, # Low temperature for more deterministic output
    )

    policy_folders = get_policy_folders(policies_dir)
    policy_index = get_policy_index(policies_dir)
    results = {}
    has_deviations = False  # Track if any deviations were found

    if not policy_folders:
        # Generate an empty report or a report indicating no policies were found
        generate_summary_report({}, puml_path, no_policies_found=True, policies_dir_path=policies_dir)
        return False  # Return False indicating no policies found

    for policy_folder in policy_folders:
        folder_name = os.path.basename(policy_folder)
        policy_id = folder_name.replace("-control", "")
        policy_description = policy_index.get(policy_id, "N/A") # Default description

        evaluation_output = evaluate_policy(puml_path, policy_folder, llm, policy_id, policy_description)

        if evaluation_output: # Check if evaluation_output is not None
            result_text, is_compliant_status = evaluation_output
            if result_text is not None: # Further check if result_text is not None
                results[policy_id] = {
                    "description": policy_description, # Keep for detailed section if needed later by user
                    "result": result_text,
                    "is_compliant": is_compliant_status
                }
                # If any policy is not compliant, mark that we found a deviation
                if not is_compliant_status:
                    has_deviations = True

    generate_summary_report(results, puml_path)
    return has_deviations  # Return whether any deviations were found

def generate_summary_report(results: dict, puml_path: str, no_policies_found: bool = False, policies_dir_path: str = ""):
    if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
        os.makedirs(REPORT_OUTPUT_DIRECTORY)

    puml_name = os.path.basename(puml_path).replace(".puml", "")
    #report_filename = f"policy_evaluation_report_{TIMESTAMP}.md"
    report_filename = "policy_evaluation_report.md"
    report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, report_filename)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Architecture Policy Evaluation Report\n\n")
        f.write(f"**Diagram**: `{os.path.basename(puml_path)}`\n")
        f.write(f"**Date**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if no_policies_found:
            f.write("## Summary of Compliance\n\n")
            f.write(f"No policy folders (e.g., ARC-POLICY-XXX-control) found in the specified policies directory: `{policies_dir_path}`.\n")
            f.write("Therefore, no policies were evaluated against this diagram.\n\n")
            return # End report generation here

        f.write("## Summary of Compliance\n\n")
        f.write("| Policy ID      | Compliance Status |\n")
        f.write("|----------------|-------------------|\n")

        # Sort results by policy ID for consistent ordering
        sorted_results = sorted(results.items(), key=lambda item: item[0])

        for policy_id, data in sorted_results:
            is_compliant = data.get("is_compliant", False)
            compliance_status_text = "✅ Yes" if is_compliant else "❌ No"
            row = f"| {policy_id}      | {compliance_status_text}    |\n"
            f.write(row)

        f.write("\n## Detailed Policy Evaluations\n\n")

        non_compliant_policies = {pid: data for pid, data in results.items() if not data.get("is_compliant", True)}
        compliant_policies = {pid: data for pid, data in results.items() if data.get("is_compliant", False)}

        if not results:
            f.write("*No policies were evaluated or found to report on.*\n\n")
        elif not non_compliant_policies and not compliant_policies: # Should not happen if results is not empty
            f.write("*No policy evaluation results available.*\n\n")

        if non_compliant_policies:
            f.write("### Non-Compliant Policies\n\n")
            # Sort non-compliant policies by ID
            for policy_id, data in sorted(non_compliant_policies.items()):
                f.write(f"#### {policy_id} - ❌ NON-COMPLIANT\n\n")
                f.write(f"**Evaluation Details:**\n")
                f.write(data.get("result", "No evaluation result available."))
                f.write("\n\n---\n\n")

        if compliant_policies:
            f.write("### Compliant Policies\n\n")
            # Sort compliant policies by ID
            for policy_id, data in sorted(compliant_policies.items()):
                f.write(f"#### {policy_id} - ✅ COMPLIANT\n\n")
                f.write(f"**Evaluation Details:**\n")
                f.write(data.get("result", "No evaluation result available."))
                f.write("\n\n---\n\n")


def main(github_repo_url):
    """Main function that handles the entire workflow"""
    repo_dir = None # Initialize repo_dir
    try:
        repo_dir = tempfile.mkdtemp()
        clone_repo(github_repo_url, repo_dir)

        policies_dir = find_policies_dir(repo_dir)
        if not policies_dir:
            if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
                os.makedirs(REPORT_OUTPUT_DIRECTORY)
            error_report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "ERROR_REPORT_policies_not_found.md")
            with open(error_report_path, "w") as erf:
                erf.write(f"# Evaluation Error\n\nFailed to find the 'policies' directory in the repository: {github_repo_url}\n")
                erf.write(f"Searched in: {repo_dir}\n")
            return False, True  # Error occurred, but treat as no deviations

        architecture_diagrams = find_architecture_diagrams(repo_dir)
        if not architecture_diagrams:
            if not os.path.exists(REPORT_OUTPUT_DIRECTORY):
                os.makedirs(REPORT_OUTPUT_DIRECTORY)
            error_report_path = os.path.join(REPORT_OUTPUT_DIRECTORY, "ERROR_REPORT_diagrams_not_found.md")
            with open(error_report_path, "w") as erf:
                erf.write(f"# Evaluation Error\n\nFailed to find any PlantUML diagrams in the repository: {github_repo_url}\n")
                erf.write(f"Searched in: {repo_dir} (specifically 'architecture' folder or any .puml files if 'architecture' doesn't exist)\n")
            return False, True  # Error occurred, but treat as no deviations
        
        first_diagram = architecture_diagrams[0]

        # Now returns whether any deviations were found
        has_deviations = evaluate_all_policies(first_diagram, policies_dir)
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
        return False, True  # Error occurred, but treat as no deviations since we can't determine otherwise
    finally:
        if repo_dir and os.path.exists(repo_dir):
            try:
                shutil.rmtree(repo_dir)
            except Exception as e:
                pass

if __name__ == "__main__":

    github_repo_url = "https://github.com/chillisurfer-one/aac-direct-debit-update"
    success, has_deviations = main(github_repo_url)

    if has_deviations:
            #Exit with code 1 if deviations were found"
            sys.exit(1)
    else:
            #Exit with code 0 if no deviations were found"
            sys.exit(0)
