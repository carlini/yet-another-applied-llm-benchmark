from evaluator import *

TAGS = ['explain']

question = """
What is the hidden dimension of LLAMA-2 70b?
"""

TestLlamaKnowledge = question >> LLMRun() >> SubstringEvaluator("8192")

if __name__ == "__main__":
    print(run_test(TestLlamaKnowledge))
