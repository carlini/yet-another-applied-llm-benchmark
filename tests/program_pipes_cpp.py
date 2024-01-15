from evaluator import *

DESCRIPTION = "Test if the model can generate a C++ program that defines dataflow DSL."

TAGS = ['code', 'c']

question = """
Write a C++ class Const, Square, Print so that I can write, for example,

Cost(5) >> Square() >> Inc() >> Print()

and the resulting python program will print 26 to the screen.
"""

test_case, answer = make_c_test([("Const(2) >> Square() >> Inc() >> Square()", "25")])

TestMakeShiftOpC = question >> LLMRun() >> ExtractCode() >> CppRun() >> SubstringEvaluator(answer)
    

if __name__ == "__main__":
    print(run_test(TestMakeShiftOpC))
