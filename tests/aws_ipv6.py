from evaluator import *

DESCRIPTION = "Test if the model can identify the error in an AWS Lambda code for authorizing a new network. This type of error is generally difficult to find via search."

TAGS = ['explain']

question = """This a code for aws lambda to authorize a new network, what is wrong with this :
security_group.authorize_egress(
            IpPermissions=[
                {'IpProtocol': '-1',
                 'IpRanges': [{'CidrIpv6': '::/0'}]}
            ]
        )
"""

answer = 'Ipv6Ranges'

TestAWSV6 = question >> LLMRun() >>  Echo()  >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestAWSV6))


