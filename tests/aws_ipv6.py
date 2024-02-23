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

evaluation = """
Below is a software engineer's answer to a request to find an issue with the following code: <A>

Does the engineer mention overly permissive IPv6 ranges? Think out loud, and then end your answer with either the string "The issue is found" or "The issue is not found".
"""

TestAWSV6 = question >> LLMRun() >> LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("The issue is found")

if __name__ == "__main__":
    print(run_test(TestAWSV6))


