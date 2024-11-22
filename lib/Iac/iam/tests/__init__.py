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

# Create the stack
AwsSSOGroupMappingStack(
    app, "AwsSSOGroupMappingStack",
    context=env_config,
    account_id=config["aws"]["AWS_ACCOUNT_ID"],
    sso_groups_permission_sets=env_config["sso_groups_permission_sets"],
    sso_groups_ids=env_config["sso_groups_ids"],
    sso_instance_arn=env_config["sso_instance_arn"]
)

app.synth()

///////////////////

import json
from aws_cdk import Stack
import aws_cdk.aws_servicecatalog as servicecatalog
from constructs import Construct

class AWSControlTowerAccountFactoryStack(Stack):
    def __init__(self, scope: Construct, id: str, account_file: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Load account details from the specified JSON file
        with open(account_file) as f:
            account = json.load(f)["account_config"]

        self.provisioned_product = servicecatalog.CfnCloudFormationProvisionedProduct(self, "myProvisionedProduct",
            product_name="AWS Control Tower Account Factory",
            provisioning_artifact_name="AWS Control Tower Account Factory",
            provisioning_parameters=[
                {"key": "AccountEmail", "value": account["AccountEmail"]},
                {"key": "AccountName", "value": account["AccountName"]},
                {"key": "ManagedOrganizationalUnit", "value": account["ManagedOrganizationalUnit"]},
                {"key": "SSOUserEmail", "value": account["SSOUserEmail"]},
                {"key": "SSOUserFirstName", "value": account["SSOUserFirstName"]},
                {"key": "SSOUserLastName", "value": account["SSOUserLastName"]}
            ]
        )