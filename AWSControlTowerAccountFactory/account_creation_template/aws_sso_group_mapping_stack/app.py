import json
import os
import re
from pathlib import Path
from aws_cdk import App
from aws_sso_group_mapping_stack import AwsSSOGroupMappingStack

# Define the path to the data folder
data_path = Path(__file__).parent.parent.parent.parent / 'AWSControlTowerAccountFactory/data'

# Initialize the CDK app
app = App()

# File path
filepath = app.node.try_get_context("filepath")

# Fallback to a default path if the context variable is not set
if filepath is None:
    filepath = data_path / 'sso-groups'

# Ensure the filepath is a string
filepath = str(filepath)

# Print the file path for debugging
print(f"File path: {filepath}")

# Check if the path is a directory or a file
if os.path.isfile(filepath):
    ssogroups_dir = os.path.dirname(filepath)
else:
    ssogroups_dir = filepath

# Check if the directory exists
if not os.path.exists(ssogroups_dir):
    raise FileNotFoundError(f"The directory {ssogroups_dir} does not exist.")

def get_account_files(directory):
    """Get a list of JSON files in the specified directory."""
    if not os.path.exists(directory):
        return []
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]

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
            new_json_path = os.path.join(output_dir, new_json_filename)
            
            with open(new_json_path, 'w') as new_json_file:
                json.dump(new_json_content, new_json_file, indent=4)

# Define the output directory for the new JSON files
output_dir = data_path / 'generated-sso-groups'
os.makedirs(output_dir, exist_ok=True)

# Get the list of account files
account_files = get_account_files(ssogroups_dir)

# Create stacks for each account file and generate new JSON files if account files exist
if account_files:
    create_stacks(app, account_files, output_dir)

# Synthesize the app
app.synth()