from evaluator import *

DESCRIPTION = "Test if the model can write a Python function that removes excess indentation from a given block of code."

TAGS = ['code', 'python']

question = """
Write a python function `dedent(str)` that takes as input a string of python code and de-dents it maximally. Lines that are entirely blank don't count.
"""

test_case, answer = make_python_test([("""dedent('''    print("hello")
    print("world")

    if True:
        print("true")
    else:
        print("false")''')""", '''"""print("hello")
print("world")

if True:
    print("true")
else:
    print("false")"""''')])


TestDedent = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestDedent))

