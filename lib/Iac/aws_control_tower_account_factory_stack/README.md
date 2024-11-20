# AWS Control Tower Account Factory

## Overview
This script automates the creation of AWS Control Tower Account Factory stacks using AWS CDK.

## Step 1 - bootstrap an AWS account using the following command
`cdk bootstrap aws://498917051903/us-east-1 --profile TCBEnterprise_RootProdPayer`
## Step 2 - Create IAM Role 
`cdk ls -c filepath=C:\Projects\KubernetesPlatform\.github\workflows\data\global\non_prod\iam\TCB_PayerAccount.v1.0.0.json --profil TCBEnterprise_RootProdPayer`

## Step 3 -  grant our CDK execution role access to the AWS Control Tower Account Factory Portfolio

 - Before using/deploying our CDK application to provision the “AWS Control Tower Account Factory”, we first need to grant our CDK execution role access to the AWS Control Tower Account Factory Portfolio by following the below steps:

 ```
    1 - Using an Admin user in your management account, go to the Service Catalog console.`
    2 - On the side panel, go to ‘Portfolios’.`
    3 - Under ‘Local portfolios’, click into the one called “AWS Control Tower Account Factory Portfolio”.`
    4 - Go to the ‘Access’ tab and click ‘Grant access’.`
    4 - Go to the ‘Roles’ tab and select our CDK execution role (by default it should have the name        ‘cdk-hnb659fds-cfn-exec-role-<Account ID>-<Region>‘) and click ‘Grant Access’.`
            `cdk-hnb659fds-cfn-exec-role-498917051903-us-east-1`
    - These steps will allow our CDK execution role to access the AWS Control Tower Account Factory Portfolio.
```
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
