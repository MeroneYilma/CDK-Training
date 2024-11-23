import json
import os
from aws_cdk import App
from aws_sso_group_mapping_stack import AwsSSOGroupMappingStack

app = App()

# FilePath
filepath = app.node.try_get_context("filepath")

# Load File
with open(filepath, 'r') as f:
    config = json.load(f)

# Extract the configuration for the specific environment
env_config = config["sso_config"]

# Extract a unique identifier for the stack name (e.g., AccountName)
if "accounts" in config and len(config["accounts"]) > 0 and "AccountName" in config["accounts"][0]:
    unique_identifier = config["accounts"][0]["AccountName"]
else:
    raise KeyError("AccountName not found in the accounts array in the JSON configuration.")

# Create the stack with a unique name
AwsSSOGroupMappingStack(
    app, f"AwsSSOGroupMappingStack-{unique_identifier}",  # Use unique identifier in stack name
    context=config,  # Pass the entire config as context
    account_id=config["aws"]["AWS_ACCOUNT_ID"],
    sso_groups_permission_sets=env_config["sso_groups_permission_sets"],
    sso_groups_ids=env_config["sso_groups_ids"],
    sso_instance_arn=env_config["sso_instance_arn"]
)

app.synth()