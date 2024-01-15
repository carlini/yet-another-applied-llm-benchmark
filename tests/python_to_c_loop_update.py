from evaluator import *

DESCRIPTION = "Test if a model can convert a python program to c, with a loop that makes it difficult."

TAGS = ['code', 'python', 'c']

question = """
Convert this to c

def foo(x):
    sum = 0
    for i in range(x):
        x += i
        sum += x
    return sum
"""

test_case, answer = make_c_test([("foo(10)", "265")])


TestPythonToCLoopUpdate = question >> LLMRun() >> ExtractCode() >> CRun(test_case) >> SubstringEvaluator(answer)
                                                                    
if __name__ == "__main__":
    print(run_test(TestPythonToCLoopUpdate))
