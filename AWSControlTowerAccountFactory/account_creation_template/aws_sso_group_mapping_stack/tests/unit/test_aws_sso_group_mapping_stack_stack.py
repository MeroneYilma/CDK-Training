import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_sso_group_mapping_stack.aws_sso_group_mapping_stack_stack import AwsSsoGroupMappingStackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_sso_group_mapping_stack/aws_sso_group_mapping_stack_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsSsoGroupMappingStackStack(app, "aws-sso-group-mapping-stack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
