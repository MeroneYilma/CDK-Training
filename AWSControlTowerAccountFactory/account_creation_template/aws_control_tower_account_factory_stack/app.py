import os
import json
from pathlib import Path
from aws_cdk import App
from aws_control_tower_account_factory_stack import AWSControlTowerAccountFactoryStack

# Define the path to the data folder
data_path = Path(__file__).parent.parent.parent.parent / 'AWSControlTowerAccountFactory/data'

def get_account_name(file_path):
    """Extract the account name from the file path and replace underscores with hyphens."""
    base_name = os.path.basename(file_path)
    name_without_extension = os.path.splitext(base_name)[0]
    return name_without_extension.replace('_', '-')

def get_account_files(directory):
    """List all JSON files in the specified directory."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")
    
    account_files = [
        os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')
    ]
    
    if not account_files:
        raise FileNotFoundError(f"No JSON files found in the directory '{directory}'.")
    
    return account_files

def set_env_variables_from_json(file_path):
    """Set environment variables from the JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        aws_data = data.get('aws', {})
        os.environ['AWS_ACCOUNT_ID'] = aws_data.get('AWS_ACCOUNT_ID', '')
        os.environ['REGION'] = aws_data.get('REGION', '')

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

def main():
    app = App()

    # Get the JSON file path from context
    filepath = app.node.try_get_context("filepath")

    if filepath:
        # Convert to absolute path relative to the project root
        abs_filepath = data_path / filepath
        
        if not abs_filepath.exists():
            raise FileNotFoundError(f"The file '{abs_filepath}' does not exist.")
        
        set_env_variables_from_json(abs_filepath)
        account_name = get_account_name(abs_filepath)
        AWSControlTowerAccountFactoryStack(
            app, 
            f"AWSControlTowerAccountFactoryStack-{account_name}", 
            account_file=abs_filepath
        )
    else:
        accounts_dir = data_path / "accounts"
        account_files = get_account_files(accounts_dir)
        create_stacks(app, account_files)

    app.synth()

if __name__ == "__main__":
    main()