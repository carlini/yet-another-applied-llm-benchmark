from evaluator import *

DESCRIPTION = "Test the knowledge cutoff of the model to see if it knows the LLAMA-2 hidden dimension size."

TAGS = ['explain']

question = """
What is the hidden dimension of LLAMA-2 70b?
"""

TestLlamaKnowledge = question >> LLMRun() >> (SubstringEvaluator("8192") | SubstringEvaluator("8,192"))

if __name__ == "__main__":
    print(run_test(TestLlamaKnowledge))
