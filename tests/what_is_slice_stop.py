from evaluator import *

DESCRIPTION = "This test case checks if the model can say how to properly get the end of a slice."

TAGS = ['explain', 'python']

question = """
How do I get sice(0, 5).end?
"""

TestWhatIsSlice = question >> LLMRun() >> SubstringEvaluator(".stop")

if __name__ == "__main__":
    print(run_test(TestWhatIsSlice))
