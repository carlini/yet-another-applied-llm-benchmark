from evaluator import *

DESCRIPTION = "Test if the model knows what ERR_BLOCKED_BY_ORB means."

TAGS = ['explain']

question = """
What does "ERR_BLOCKED_BY_ORB" mean?
"""

TestWhatIsBlockByOrb = question >> LLMRun() >> SubstringEvaluator("opaque resource blocking", lower=True)

if __name__ == "__main__":
    print(run_test(TestWhatIsBlockByOrb))

