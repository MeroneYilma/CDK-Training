from aws_cdk import (
    Stack,
    Tags,
    CfnTag,
    CfnOutput,
    aws_iam as iam
)
from constructs import Construct

class IamStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, iam_config: dict, tags: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Use the existing OIDC provider
        oidc_provider_arn = iam_config.get('oidc_provider_arn')
        if oidc_provider_arn:
            self.oidc_provider = iam.CfnOIDCProvider.from_oidc_provider_arn(self, 'ExistingOIDCProvider', oidc_provider_arn)
        else:
            self.oidc_provider = iam.CfnOIDCProvider(self, iam_config['oidc_provider_name'],
                client_id_list = [iam_config['client_id']],
                tags=[CfnTag(
                    key="Name",
                    value=iam_config['oidc_provider_name']
                )],
                thumbprint_list = iam_config['thumbprint_list'],
                url = iam_config['url']
            )

        self.cfn_role = iam.CfnRole(self, iam_config['role_name'],
            assume_role_policy_document = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Federated": self.oidc_provider.attr_arn
                        },
                        "Action": "sts:AssumeRoleWithWebIdentity",
                        "Condition": {
                            "StringEquals": {
                                "token.actions.githubusercontent.com:aud": iam_config['client_id']
                            },
                            "StringLike": {
                                "token.actions.githubusercontent.com:sub": iam_config['github_repo']
                            }
                        }
                    }
                ]
            },
            description=iam_config['description'],
            managed_policy_arns = iam_config['managed_policy_arns'],
            role_name = iam_config['role_name'],
            tags=[CfnTag(
                key="Name",
                value=iam_config['role_name']
            )]
        )

        # Apply additional tags to the GitHub Action Assume Role and OIDC Provider
        for key, value in tags.items():
            Tags.of(self.oidc_provider).add(key, value)
            Tags.of(self.cfn_role).add(key, value)

        # Export the OIDC Provider ARN
        CfnOutput(self, f"{construct_id}-OIDCProviderArn", 
                  value=self.oidc_provider.attr_arn, 
                  export_name=f"{construct_id}-OIDCProviderArn")  
        
        # Export the GitHub Action Assume Role ARN
        CfnOutput(self, f"{construct_id}-GitHubActionAssumeRoleArn", 
                  value=self.cfn_role.attr_arn, 
                  export_name=f"{construct_id}-GitHubActionAssumeRoleArn")