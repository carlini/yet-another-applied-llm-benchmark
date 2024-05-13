from evaluator import *

DESCRIPTION = "Test if the model can generate a C++ program that defines dataflow DSL."

TAGS = ['code', 'c']

question = """
Write a C++ class Const, Square, Print so that I can write, for example,

Cost(5) >> Square() >> Inc() >> Inc() >> Print()

and the resulting python program will print 27 to the screen.
"""

test_case = """int main() {
Const(2) >> Square() >> Inc() >> Square() >> Square() >> Print();
return 0;
}"""


TestMakeShiftOpC = question >> LLMRun() >> ExtractCode() >> CppRun(test_case) >> SubstringEvaluator("625")
    

if __name__ == "__main__":
    print(run_test(TestMakeShiftOpC))
