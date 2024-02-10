from evaluator import *

DESCRIPTION = "Test if a model knows how to get the HTML for the entire webpage; not just the body."

TAGS = ['explain', 'html']

question = """
I have a webpage that's open in a chrome browser but the page no longer exists. What javascript should I type in the console to get a copy of the entire page html?
"""

TestRecoverExpiredPage = question >> LLMRun() >> SubstringEvaluator("outerHTML")

if __name__ == "__main__":
    print(run_test(TestRecoverExpiredPage))

