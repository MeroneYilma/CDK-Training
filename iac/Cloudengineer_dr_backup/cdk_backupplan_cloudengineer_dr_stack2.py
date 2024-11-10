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

class CdkBackupplanCloudengineerDrStack2(Stack):

    def __init__(self, scope: Construct, id: str, *, 
                 secondary_backup_vault_arn: str, 
                 secondary_backup_vault_encryption_key_arn: str, 
                 main_backup_stack_encryption_key_arn: str, 
                 main_backup_vault_name: str,  # Corrected parameter name
                 backup_plan_name_2: str, 
                 backup_plan_rule_name_2: str, 
                 backup_selection_resource_arn: str, 
                 main_backup_vault_iam_role: list,
                 backup_resource_selection_iam_role: str,
                 selection_name_2: str,  # Add the new parameter
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Reference the existing backup vault
        backup_vault = backup.BackupVault.from_backup_vault_name(self, "BackupVault", main_backup_vault_name)
        
        # Define the backup plan with copy action
        backup_plan = backup.CfnBackupPlan(self, "BackupPlan2",
            backup_plan={
                "backupPlanName": backup_plan_name_2,
                "backupPlanRule": [{
                    "ruleName": backup_plan_rule_name_2,
                    "targetBackupVault": backup_vault.backup_vault_name,
                    "scheduleExpression": "cron(0 12 1 * ? *)",  # Will run the the first day of every monthly at 12:00 UTC
                    "startWindowMinutes": 60,
                    "completionWindowMinutes": 120,
                    "lifecycle": {
                        "deleteAfterDays": 30
                    },
                    "copyActions": [{
                        "destinationBackupVaultArn": secondary_backup_vault_arn,
                        "lifecycle": {
                            "deleteAfterDays": 180
                        }
                    }],
                    "enableContinuousBackup": True  # Enable continuous backups for PITR
                }]
            }
        )

        # Define the backup selection
        backup_selection = backup.CfnBackupSelection(self, "BackupSelection2",
            backup_plan_id=backup_plan.ref,
            backup_selection={
                "selectionName": selection_name_2,  # Use the context variable here
                "iamRoleArn": backup_resource_selection_iam_role,
                "resources": [
                    backup_selection_resource_arn  # Ensure this ARN is specific to RDS instances
                ]
            }
        )