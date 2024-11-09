#!/usr/bin/env python3
import os
import json
import aws_cdk as cdk
from iam.iam_stack import IamStack

app = cdk.App()

# FilePath
filepath = app.node.try_get_context("filepath")

# Ensure the filepath is a string
if filepath is None:
    raise ValueError("The 'filepath' context variable is not set.")

# Check if the file exists
if not os.path.exists(filepath):
    raise FileNotFoundError(f"The file {filepath} does not exist.")

# Load File
with open(filepath, 'r') as f:
    config = json.load(f)

# Extract the configuration for the specific environment
env_config = config["iam_config"]

# Define the environment (account and region)
env = cdk.Environment(account=env_config["account_id"], region=env_config["region"])

# Create the iam stack with the loaded configuration
if env_config.get("deploy_iam_stack", False):
    iam_stack = IamStack(app, env_config["iam_stack_name"],
                         iam_config=env_config["iam"],
                         tags=env_config["tags"],
                         env=env)
    
app.synth()