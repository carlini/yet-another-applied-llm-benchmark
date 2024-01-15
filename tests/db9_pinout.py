from evaluator import *

DESCRIPTION = "Test if a model knows about old computer ports when prompted ambiguously."

TAGS = ['explain']

question = """
What port has 5 pins on the top and 4 on the bottom?
"""

TestDB9 = question >> LLMRun() >> (SubstringEvaluator("DB-9") | SubstringEvaluator("DB9") | SubstringEvaluator("DE-9") | SubstringEvaluator("DE9"))

if __name__ == "__main__":
    print(run_test(TestDB9))
