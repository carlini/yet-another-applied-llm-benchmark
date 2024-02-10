from evaluator import *

DESCRIPTION = "Test if the model knows how to use the strided trick with numpy."

TAGS = ['code', 'python', 'performance']

question = """
Write a function strides() that given an array of tokens T as numpy array, using strided trick, returns [T[0:50], T[10:60], T[20: 70] ... ]
"""

test_case, answer = make_python_test([("strides(np.arange(100)).shape", "(6, 50)"),
                                     ("strides(np.arange(100)).sum()", "14850")])

TestProgramStrided = question >> LLMRun() >> ExtractCode() >> ((PythonRun(test_case) >> (SubstringEvaluator(answer))) & SubstringEvaluator("as_strided"))

if __name__ == "__main__":
    print(run_test(TestProgramStrided))
