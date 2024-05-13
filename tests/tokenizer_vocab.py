from evaluator import *

DESCRIPTION = "This test case is designed to check if the model can print out the tokens in a AutoTokenizer's vocabulary."

TAGS = ['explain', 'python']

question = """
How do I get all tokens in a AutoTokenizer?
"""

TestGetVocab = question >> LLMRun() >> SubstringEvaluator("get_vocab")

if __name__ == "__main__":
    print(run_test(TestGetVocab))

