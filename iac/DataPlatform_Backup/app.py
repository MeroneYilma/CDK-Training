import json
from pathlib import Path
from aws_cdk import App
from cdk_backupplan_dataplatform_stack import CdkBackupplanDataPlatformStack
from cdk_backupplan_dataplatform_stack2 import CdkBackupplanDataPlatformStack2
from secondarybackup_dataplatform_vault_stack import SecondarybackupDataPlaformVaultStack

# Define the path to the data folder ### In the treasury account
data_path = Path(__file__).parents[2] / '.github/data/dataplatform'

# Load JSON configurations
def load_config(file_name):
    config_file_path = data_path / file_name
    print(f"Loading configuration from: {config_file_path}")
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)

config_main_backup = load_config('main_backup.json')
print("Main Backup Config:", json.dumps(config_main_backup, indent=4))

config_backup_plan_2 = load_config('backup_plan_2.json')
print("Backup Plan 2 Config:", json.dumps(config_backup_plan_2, indent=4))

config_secondary_backup = load_config('secondary_backup.json')
print("Secondary Backup Config:", json.dumps(config_secondary_backup, indent=4))

# Load the backup vault policy
backup_vault_policy_path = data_path / 'backup_vault_policy.json'
print(f"Loading backup vault policy from: {backup_vault_policy_path}")
with open(backup_vault_policy_path, 'r') as policy_file:
    backup_vault_policy = json.load(policy_file)
print("Backup Vault Policy:", json.dumps(backup_vault_policy, indent=4))

app = App()

# Instantiate stacks with configuration
CdkBackupplanDataPlatformStack(app, "CdkBackupplanDataPlatformStack",
                   secondary_backup_vault_arn=config_backup_plan_2['secondary_backup_vault_arn'],
                   secondary_backup_vault_encryption_key_arn=config_backup_plan_2['secondary_backup_vault_encryption_key_arn'],
                   main_backup_stack_encryption_key_arn=config_main_backup['stack_encryption_key_arn'],
                   backup_vault_name=config_main_backup['vault_name'],
                   backup_plan_name=config_main_backup['plan_name'],
                   backup_plan_rule_name=config_main_backup['plan_rule_name'],
                   backup_selection_resource_arn=config_main_backup['selection_resource_arn'],
                   main_backup_vault_iam_role=config_main_backup['vault_iam_role'],
                   backup_resource_selection_iam_role=config_main_backup['resource_selection_iam_role'],
                   selection_name=config_main_backup['selection_name'])

CdkBackupplanDataPlatformStack2(app, "CdkBackupplanDataPlatformStack2",
                    secondary_backup_vault_arn=config_backup_plan_2['secondary_backup_vault_arn'],
                    secondary_backup_vault_encryption_key_arn=config_backup_plan_2['secondary_backup_vault_encryption_key_arn'],
                    main_backup_stack_encryption_key_arn=config_backup_plan_2['main_backup_stack_encryption_key_arn'],
                    main_backup_vault_name=config_backup_plan_2['main_backup_vault_name'],
                    backup_plan_name_2=config_backup_plan_2['backup_plan_name_2'],
                    backup_plan_rule_name_2=config_backup_plan_2['backup_plan_rule_name_2'],
                    backup_selection_resource_arn=config_backup_plan_2['backup_selection_resource_arn'],
                    main_backup_vault_iam_role=config_backup_plan_2['main_backup_vault_iam_role'],
                    backup_resource_selection_iam_role=config_backup_plan_2['backup_resource_selection_iam_role'],
                    selection_name_2=config_backup_plan_2['selection_name_2'])

SecondarybackupDataPlaformVaultStack(app, "SecondarybackupDataPlaformVaultStack",
                          backup_vault_name=config_secondary_backup['vault_name'],
                          backup_role_arn=config_secondary_backup['backup_role_arn'],
                          secondary_backup_vault_encryption_key_arn=config_secondary_backup['secondary_backup_vault_encryption_key_arn'],
                          backup_vault_policy=backup_vault_policy)

app.synth()