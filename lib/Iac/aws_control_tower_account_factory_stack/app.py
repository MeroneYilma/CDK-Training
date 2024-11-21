import os
import json
import aws_cdk as cdk
from aws_control_tower_account_factory_stack import AWSControlTowerAccountFactoryStack

app = cdk.App()

# FilePath
filepath = app.node.try_get_context("filepath")

if not filepath:
    raise ValueError("The 'filepath' context parameter is required.")

# Load File
with open(filepath, 'r') as f:
    config = json.load(f)

# Extract the configuration for the specific environment
aws_config = config["aws"]

# Define the environment (optional)
env = cdk.Environment(account=aws_config["AWS_ACCOUNT_ID"], region=aws_config["REGION"])

# Create a unique stack name for the account
account_config = config["account_config"]
stack_name = f"AWSControlTowerAccountFactoryStack-{account_config['AccountName'].replace('_', '-')}"

# Instantiate the stack
AWSControlTowerAccountFactoryStack(app, stack_name, account_file=filepath, env=env)

app.synth()