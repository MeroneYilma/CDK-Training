import re
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

        for group_name, permission_set_arn in sso_groups_permission_sets.items():
            group_id = sso_groups_ids.get(group_name)
            if group_id not in validated_group_ids:
                print(f"Validating group ID: {group_id} for group name: {group_name}")  # Debugging information
                if not group_id:
                    raise KeyError(f"Group ID for {group_name} not found in sso_groups_ids")
                if not self._is_valid_group_id(group_id):
                    raise ValueError(f"Invalid SSO group ID: {group_id}")
                validated_group_ids.add(group_id)
            sso.CfnAssignment(
                self, f"{group_name}-{account_id}",
                instance_arn=sso_instance_arn,
                target_id=account_id,
                target_type="AWS_ACCOUNT",
                principal_id=group_id,
                principal_type="GROUP",
                permission_set_arn=permission_set_arn
            )

    def _is_valid_group_id(self, group_id: str) -> bool:
        # Adjusted pattern to match the provided group IDs
        pattern = re.compile(r'^[a-f0-9-]+$')
        return bool(pattern.match(group_id))