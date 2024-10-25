import aws_cdk as core
import aws_cdk.assertions as assertions

from account_creation_template.account_creation_template_stack import AccountCreationTemplateStack

# example tests. To run these tests, uncomment this file along with the example
# resource in account_creation_template/account_creation_template_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AccountCreationTemplateStack(app, "account-creation-template")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
