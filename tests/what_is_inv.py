from evaluator import *

DESCRIPTION = "This test case is designed to check if the model can correctly identify the Python operator used for the tilde (~) symbol."

TAGS = ['explain', 'python']

question = """
In python what __thing__ do I use for ~, kind of like how __add__ is for +?
"""

TestWhatIsInv = question >> LLMRun() >> (SubstringEvaluator("__inv__") | SubstringEvaluator("__invert__"))

if __name__ == "__main__":
    print(run_test(TestWhatIsInv))
