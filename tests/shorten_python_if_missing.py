from evaluator import *

DESCRIPTION = "Test if the model can shorten a line of python with an equal line."

TAGS = ['code', 'python']

question = """
Shorten this python code. Keep the name the same.
```
def foo(arr, keys):
    return [[x[y] if y in x else -5 for y in keys] for x in arr]
```
"""

test_case, answer = make_python_test([("foo([{1: 2, 3: 4, 5: 6}], [1, 2, 3, 4])", "[[2, -5, 4, -5]]")])

TestShortenPyGet = question >> LLMRun() >> (SubstringEvaluator(".get") & (ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator(answer)))

                                            

if __name__ == "__main__":
    print(run_test(TestShortenPyGet))

