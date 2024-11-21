import json
import os
from aws_cdk import App
from aws_sso_group_mapping_stack import AwsSSOGroupMappingStack

app = App()

# FilePaths
filepaths = app.node.try_get_context("filepaths")

# Ensure filepaths is a list
if not isinstance(filepaths, list):
    raise ValueError("The context parameter 'filepaths' must be a list of file paths.")

# Load and merge files
merged_config = {
    "sso_config": {
        "sso_groups_permission_sets": [],
        "sso_groups_ids": [],
        "sso_instance_arn": None
    },
    "aws": {
        "AWS_ACCOUNT_ID": None
    }
}

for filepath in filepaths:
    with open(filepath, 'r') as f:
        config = json.load(f)
        if merged_config["aws"]["AWS_ACCOUNT_ID"] is None:
            merged_config["aws"]["AWS_ACCOUNT_ID"] = config["aws"]["AWS_ACCOUNT_ID"]
        if merged_config["sso_config"]["sso_instance_arn"] is None:
            merged_config["sso_config"]["sso_instance_arn"] = config["sso_config"]["sso_instance_arn"]
        merged_config["sso_config"]["sso_groups_permission_sets"].extend(config["sso_config"]["sso_groups_permission_sets"])
        merged_config["sso_config"]["sso_groups_ids"].extend(config["sso_config"]["sso_groups_ids"])

# Extract the configuration for the specific environment
env_config = merged_config["sso_config"]

# Create the stack
AwsSSOGroupMappingStack(
    app, "AwsSSOGroupMappingStack",
    context=env_config,
    account_id=merged_config["aws"]["AWS_ACCOUNT_ID"],
    sso_groups_permission_sets=env_config["sso_groups_permission_sets"],
    sso_groups_ids=env_config["sso_groups_ids"],
    sso_instance_arn=env_config["sso_instance_arn"]
)

app.synth()