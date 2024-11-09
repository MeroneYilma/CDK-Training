import aws_cdk as core
import aws_cdk.assertions as assertions

from iam.iam_stack import IamStack

# example tests. To run these tests, uncomment this file along with the example
# resource in iam/iam_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IamStack(app, "iam")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
