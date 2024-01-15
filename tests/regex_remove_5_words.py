from evaluator import *

DESCRIPTION = "Test if the model can write a Python function with a straightforward regex."

TAGS = ['code', 'python']

question = """
Write a function called `match` in Python that uses a regex to find any word repeated 5 times or more. Return that word. If no word is repeated 5 times or more, return an empty string.
"""

test_case, answer = make_python_test([("match('hi hi hi hi hi')", '"hi"'),
                                      ("match('hi hi hi hi')", '""'),
                                      ("match('hello this is is is is is a test')", '"is"')])


TestRegex = question >> LLMRun() >> ExtractCode(keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestRegex))
