import re
import boto3
from aws_cdk import (
    Stack,
    aws_sso as sso,
    aws_iam as iam,
)
from constructs import Construct

class AwsSSOGroupMappingStack(Stack):

    def __init__(self, scope: Construct, id: str, context: dict, account_id: str, sso_groups_permission_sets: dict, sso_groups_ids: dict, sso_instance_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define IAM role with necessary policies
        role = iam.Role(
            self, "SSOProvisioningRole",
            assumed_by=iam.ServicePrincipal("sso.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ]
        )

        # Attach custom policy
        role.add_to_policy(iam.PolicyStatement(
            actions=[
                "sso:CreateAssignment",
                "sso:DeleteAssignment",
                "sso:DescribeAssignment",
                "sso:ListAssignments",
                "sso:ProvisionPermissionSet",
                "sso:ListPermissionSets",
                "sso:ListPermissionSetsProvisionedToAccount",
                "sso:ListAccountsForProvisionedPermissionSet",
                "sso:ListInstances",
                "sso:ListGroupsForUser",
                "sso:ListUsers",
                "sso:ListGroups",
                "sso:DescribePermissionSet",
                "sso:DescribePermissionSetProvisioningStatus"
            ],
            resources=["*"]
        ))

        validated_group_ids = set()

        # Initialize Boto3 client for SSO
        sso_client = boto3.client('sso-admin')

        # Extract the target account ID from the context
        if "accounts" in context and len(context["accounts"]) > 0 and "AccountId" in context["accounts"][0]:
            target_account_id = context["accounts"][0]["AccountId"]
        else:
            raise KeyError("AccountId not found in the accounts array in the JSON configuration.")

        for group_name, permission_set_arn in sso_groups_permission_sets.items():
            group_id = sso_groups_ids.get(group_name)
            if group_id not in validated_group_ids:
                print(f"Validating group ID: {group_id} for group name: {group_name}")  # Debugging information
                if not group_id:
                    raise KeyError(f"Group ID for {group_name} not found in sso_groups_ids")
                if not self._is_valid_group_id(group_id):
                    raise ValueError(f"Invalid SSO group ID: {group_id}")
                validated_group_ids.add(group_id)
            
            # Check if the assignment already exists for the specific target account
            if not self._sso_assignment_exists(sso_client, sso_instance_arn, target_account_id, permission_set_arn, group_id):
                try:
                    sso.CfnAssignment(
                        self, f"{group_name}-{target_account_id}",
                        instance_arn=sso_instance_arn,
                        target_id=target_account_id,
                        target_type="AWS_ACCOUNT",
                        principal_id=group_id,
                        principal_type="GROUP",
                        permission_set_arn=permission_set_arn
                    )
                except Exception as e:
                    print(f"Error creating assignment for group {group_name}: {e}")
            else:
                print(f"Assignment for group {group_name} already exists for account {target_account_id}, skipping creation.")

    def _is_valid_group_id(self, group_id: str) -> bool:
        # Adjusted pattern to match the provided group IDs
        pattern = re.compile(r'^[a-f0-9-]+$')
        return bool(pattern.match(group_id))

    def _sso_assignment_exists(self, sso_client, instance_arn, account_id, permission_set_arn, group_id):
        try:
            response = sso_client.list_account_assignments(
                InstanceArn=instance_arn,
                AccountId=account_id,
                PermissionSetArn=permission_set_arn
            )
            for assignment in response['AccountAssignments']:
                if assignment['PrincipalId'] == group_id:
                    return True
        except Exception as e:
            print(f"Error checking assignment existence for group {group_id} in account {account_id}: {e}")
        return False