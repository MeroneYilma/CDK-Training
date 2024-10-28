# AWS Control Tower Account Factory

## Overview
This script automates the creation of AWS Control Tower Account Factory stacks using AWS CDK.


# app.py 

## Features
- Reads JSON files containing account information.
- Sets environment variables from JSON files.
- Creates AWS Control Tower Account Factory stacks for each account.

## Requirements
- Python 3.x
- AWS CDK
- JSON files with specific keys

## Usage
1. **Install Dependencies**
   - Ensure you have Python 3.x installed.
   - Install AWS CDK: `npm install -g aws-cdk`

2. **Directory Structure**
   - Place your JSON files in the `accounts` directory.

3. **Run the Script**
   - Execute the script to create stacks:
     ```sh
     python your_script.py
     ```

## JSON File Requirements
Each JSON file should contain the following keys:
- `aws`
  - `AWS_ACCOUNT_ID`
  - `REGION`
- `cdk`
  - `working_directory`
- `AccountId`
- `AccountEmail`
- `AccountName`
- `ManagedOrganizationalUnit`
- `SSOUserEmail`
- `SSOUserFirstName`
- `SSOUserLastName`

## Example JSON Structure
```json
{
    "aws": {
        "AWS_ACCOUNT_ID": "209479296537",
        "REGION": "us-east-1"
    },
    "cdk": {
        "working_directory": "account_creation_template/aws_control_tower_account_factory_stack"
    },
    "AccountId": "",
    "AccountEmail": "jacobdag0408+DemoAccount5@gmail.com",
    "AccountName": "Demo_Account5",
    "ManagedOrganizationalUnit": "Prod (ou-jw9q-k5tw4sb3)",
    "SSOUserEmail": "meroneyilma37@gmail.com",
    "SSOUserFirstName": "Merone",
    "SSOUserLastName": "Yilma"
}
```


To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
