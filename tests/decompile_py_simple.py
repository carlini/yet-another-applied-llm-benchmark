from evaluator import *

DESCRIPTION = "Test if the model can disassemble a simple Python function from its bytecode."

TAGS = ['code', 'python']

question = """
Disassemble the following python into a function called foo:

 56           0 LOAD_FAST                0 (a)
              2 LOAD_FAST                1 (b)
              4 LOAD_FAST                0 (a)
              6 BINARY_MULTIPLY
              8 BINARY_ADD
             10 RETURN_VALUE

"""

test_case, answer = make_python_test([("foo(5, 7)", "5+7*5")])


TestDisas1 = question >> LLMRun() >> ExtractCode(keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestDisas1))
