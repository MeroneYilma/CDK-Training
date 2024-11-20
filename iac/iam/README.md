
# Welcome to your CDK Python project!

## BackupVault IAM Role (make sure the us-east-1 region for the account in question is bootsraped)
- Step 1 - `cdk bootstrap --profile BackupVault_East aws://235712742900/us-east-1`
- Step 2 - `cdk deploy -c filepath=C:\CloudRepo\cloud.cdk.poc\.github\workflows\non_prod\iam\TCB_BackupVaultAccount.json --profile milu_treasury`
- Step 3 = Verify the IAm Role Trust Relationship shows the correct repo
    ```
        {
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Principal": {
				"Federated": "arn:aws:iam::364507823571:oidc-provider/token.actions.githubusercontent.com"
			},
			"Action": "sts:AssumeRoleWithWebIdentity",
			"Condition": {
				"StringEquals": {
					"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
				},
				"StringLike": {
					"token.actions.githubusercontent.com:sub": "repo:TCB-Enterprise-Cloud/cloud.iac.cdk:*"
				}
			}
		}
	]
}

```

This is a blank project for CDK development with Python.

npm install -g aws-cdk 
cdk init app --language python  
python -m venv .env  
. .\.env\Scripts\Activate 
pip install -r requirements.txt 
pip install aws-cdk-lib 


## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!