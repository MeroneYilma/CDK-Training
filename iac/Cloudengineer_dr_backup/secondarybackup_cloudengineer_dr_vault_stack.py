import json
from aws_cdk import (
    Stack,
    aws_backup as backup,
    aws_iam as iam
)
from constructs import Construct

class SecondarybackupCloudengineerDrVaultStack(Stack):

    def __init__(self, scope: Construct, id: str, *,
                 backup_vault_name: str,
                 backup_role_arn: str,
                 secondary_backup_vault_encryption_key_arn: str,
                 backup_vault_policy: dict,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Ensure backup_role_arn is not None
        if backup_role_arn is None:
            raise ValueError("The 'backup_role_arn' parameter is not defined. Please provide a valid ARN.")

        # Retrieve the IAM role from the ARN
        backup_role = iam.Role.from_role_arn(self, "BackupRole", role_arn=backup_role_arn)

        # Define the secondary backup vault
        backup_vault = backup.CfnBackupVault(self, "SecondaryBackupVault",
            backup_vault_name=backup_vault_name,
            encryption_key_arn=secondary_backup_vault_encryption_key_arn,
        )

        # Attach the IAM role to the backup vault
        backup_vault.add_property_override("AccessPolicy", backup_vault_policy)