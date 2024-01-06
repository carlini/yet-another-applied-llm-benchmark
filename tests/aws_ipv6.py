from evaluator import *

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

TestImgResize = question >> LLMRun() >>  Echo()  >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestImgResize))


