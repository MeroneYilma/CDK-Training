import json
from aws_cdk import Stack
import aws_cdk.aws_servicecatalog as servicecatalog
from constructs import Construct

class AWSControlTowerAccountFactoryStack(Stack):
    def __init__(self, scope: Construct, id: str, account_file: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Load account details from the specified JSON file
        with open(account_file) as f:
            account = json.load(f)

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