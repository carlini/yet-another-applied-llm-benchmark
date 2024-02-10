from evaluator import *

DESCRIPTION = "This test case checks if the model knows what latex package to import for the Sbox environment to work."

TAGS = ['explain']

question = """
What latex package has the Sbox env?
"""

TestWhereIsSbox = question >> LLMRun() >> SubstringEvaluator("fancybox")

if __name__ == "__main__":
    print(run_test(TestWhereIsSbox))
