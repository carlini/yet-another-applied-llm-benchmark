from evaluator import *

DESCRIPTION = "This test case checks if models can format f strings with floats."

TAGS = ['explain', 'python']

question = """
Python format {sdf} to 3 decimal digits
"""

TestWhatIsFloatFormat = question >> LLMRun() >> SubstringEvaluator(":.3f}")

if __name__ == "__main__":
    print(run_test(TestWhatIsFloatFormat))
