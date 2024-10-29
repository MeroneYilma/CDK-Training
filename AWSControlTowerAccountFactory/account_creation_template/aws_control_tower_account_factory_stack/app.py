import os
import json
from pathlib import Path
from aws_cdk import App
from aws_control_tower_account_factory_stack import AWSControlTowerAccountFactoryStack

# Define the path to the data folder
data_path = Path(__file__).parent.parent.parent.parent / '.github/data/accounts'

# Load JSON configurations
def load_config(file_name):
    config_file_path = data_path / file_name
    with open(config_file_path, 'r') as config_file:
        return json.load(config_file)

config_Demo_Account5 = load_config('Demo_Account5.json')
config_Demo_Account9 = load_config('Demo_Account9.json')
config_Demo_Account10 = load_config('Demo_Account10.json')
config_Demo_Account11 = load_config('Demo_Account11.json')

def get_account_name(file_path):
    """Extract the account name from the file path and replace underscores with hyphens."""
    base_name = os.path.basename(file_path)
    name_without_extension = os.path.splitext(base_name)[0]
    return name_without_extension.replace('_', '-')

def set_env_variables_from_json(file_path):
    """Set environment variables from the JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        aws_data = data.get('aws', {})
        os.environ['AWS_ACCOUNT_ID'] = aws_data.get('AWS_ACCOUNT_ID', '')
        os.environ['REGION'] = aws_data.get('REGION', '')

app = App()

def create_stacks(app, account_files):
    """Create a stack for each account JSON file."""
    for account_file in account_files:
        set_env_variables_from_json(account_file)
        account_name = get_account_name(account_file)
        AWSControlTowerAccountFactoryStack(
            app, 
            f"AWSControlTowerAccountFactoryStack-{account_name}", 
            account_file=account_file
        )
    app.synth()

def main():
    account_files = [str(f) for f in data_path.glob('*.json')]
    if account_files:
        create_stacks(app, account_files)
    else:
        print("No account files found.")

if __name__ == "__main__":
    main()