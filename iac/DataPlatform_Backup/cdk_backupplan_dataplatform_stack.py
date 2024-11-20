from aws_cdk import (
    Stack,
    aws_backup as backup,
    aws_iam as iam,
    aws_kms as kms,
    aws_s3 as s3,
    aws_sns as sns,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct

class CdkBackupplanDataPlatformStack(Stack):

    def __init__(self, scope: Construct, id: str, *, 
                 secondary_backup_vault_arn: str,
                 secondary_backup_vault_encryption_key_arn: str,
                 main_backup_stack_encryption_key_arn: str,
                 backup_vault_name: str,
                 backup_plan_name: str,
                 backup_plan_rule_name: str,
                 backup_selection_resource_arn: str,
                 main_backup_vault_iam_role: list,
                 backup_resource_selection_iam_role: str,
                 selection_name: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the backup vault
        backup_vault = backup.CfnBackupVault(self, "BackupVault",
            backup_vault_name=backup_vault_name,
            encryption_key_arn=main_backup_stack_encryption_key_arn
        )

        # Define the backup plan with copy action
        backup_plan = backup.CfnBackupPlan(self, "BackupPlan",
            backup_plan={
                "backupPlanName": backup_plan_name,
                "backupPlanRule": [{
                    "ruleName": backup_plan_rule_name,
                    "targetBackupVault": backup_vault.ref,
                    "scheduleExpression": "cron(0 * * * * *)",  # Every hour at minute 0
                    "startWindowMinutes": 60,
                    "completionWindowMinutes": 120,
                    "lifecycle": {
                        "deleteAfterDays": 14
                    },
                    "copyActions": [{
                        "destinationBackupVaultArn": secondary_backup_vault_arn,
                        "lifecycle": {
                            "deleteAfterDays": 30
                        }
                    }],
                    "enableContinuousBackup": True  # Enable continuous backups for PITR
                }]
            }
        )

        # Define the backup selection
        backup_selection = backup.CfnBackupSelection(self, "BackupSelection",
            backup_plan_id=backup_plan.ref,
            backup_selection={
                "selectionName": selection_name,  # Use the context variable here
                "iamRoleArn": backup_resource_selection_iam_role,
                "resources": [
                    backup_selection_resource_arn  # Ensure this ARN is specific to RDS instances
                ]
            }
        )