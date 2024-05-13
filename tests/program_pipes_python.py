from evaluator import *

DESCRIPTION = "Test if the model can generate a python program that defines dataflow DSL."

TAGS = ['code', 'python']

question = """
Write a python class Const, Square, Print so that I can write, for example,

Cost(5) >> Square() >> Inc() >> Inc() >> Print()

and the resulting python program will print 27 to the screen.
"""

test_case, answer = make_python_test([("Const(2) >> Square() >> Inc() >> Square() >> Square() >> Print()", "0")])

TestMakeShiftOp = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator("625")


if __name__ == "__main__":
    print(run_test(TestMakeShiftOp))
