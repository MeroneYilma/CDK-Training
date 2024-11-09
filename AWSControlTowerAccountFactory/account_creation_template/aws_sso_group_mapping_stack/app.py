import json
import os
import re
from pathlib import Path
from aws_cdk import App
from aws_sso_group_mapping_stack import AwsSSOGroupMappingStack

# Define the path to the data folder
data_path = Path(__file__).parent.parent.parent.parent / '.github/data/sso-groups'

# Load JSON configurations
def load_config(file_name):
    config_file_path = data_path / file_name
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)

config_Demo_Account5_sso = load_config('Demo_Account5_sso.json')
config_Demo_Account9_sso= load_config('Demo_Account9_sso.json')
config_Demo_Account10_sso = load_config('Demo_Account10_sso.json')
config_Demo_Account11_sso = load_config('Demo_Account11_sso.json')
config_Demo_Account12_sso = load_config('Demo_Account12_sso.json')

# Initialize the CDK app
app = App()

def sanitize_stack_name(name):
    """Sanitize the stack name to match the required pattern."""
    return re.sub(r'[^A-Za-z0-9-]', '-', name)

def create_stacks(app, account_files, output_dir):
    """Create stacks for each account in the JSON files and generate new JSON files."""
    for json_file_path in account_files:
        with open(json_file_path, 'r') as file:
            context = json.load(file)
        
        # Check if the required keys are present in the JSON file
        required_keys = ["sso_groups_permission_sets", "sso_groups_ids", "sso_instance_arn", "aws", "accounts"]
        if not all(key in context for key in required_keys):
            continue
        
        # Create a stack for each account in the JSON file
        for account in context["accounts"]:
            stack_name = f"AwsssoGroupMappingStack-{sanitize_stack_name(account['AccountName'])}"
            AwsSSOGroupMappingStack(
                app, stack_name,
                context=context,
                account_id=account["AccountId"],
                sso_groups_permission_sets=context["sso_groups_permission_sets"],
                sso_groups_ids=context["sso_groups_ids"],
                sso_instance_arn=context["sso_instance_arn"]
            )
            
            # Create a new JSON file for each account
            new_json_content = {
                "aws": context["aws"],
                "cdk": context["cdk"],
                "account": account,
                "sso_groups_permission_sets": context["sso_groups_permission_sets"],
                "sso_groups_ids": context["sso_groups_ids"],
                "sso_instance_arn": context["sso_instance_arn"]
            }
            new_json_filename = f"{sanitize_stack_name(account['AccountName'])}.json"
            new_json_path = output_dir / new_json_filename
            
            with open(new_json_path, 'w') as new_json_file:
                json.dump(new_json_content, new_json_file, indent=4)

# Define the output directory for the new JSON files
output_dir = data_path / 'generated-sso-groups'
output_dir.mkdir(parents=True, exist_ok=True)

# Define account_files by listing JSON files in the data_path directory
account_files = list(data_path.glob('*.json'))

# Create stacks for each account file and generate new JSON files if account files exist
if account_files:
    create_stacks(app, account_files, output_dir)

# Synthesize the app
app.synth()