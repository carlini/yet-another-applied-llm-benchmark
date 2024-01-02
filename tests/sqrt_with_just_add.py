from evaluator import *

question = """
Write some Python code to compute the square root of a real number only by calling add or subtract or comparisons with constants. Call the function my_sqrt().
"""

test_case, answer = make_python_test([("round(my_sqrt(16), 1)", "4")])

evaluation = """
Below is a student's answer to a question on implementing sqrt using only + and - operators. <A>

List out each of the following operators one by one, and check if the student uses them: multiply (*), divide (/), inline exponent (**), sqrt(), pow(), exp(), abs(). End your answer with either the string "The student passes" if they used none, or "The student fails" if they used any.
"""

TestProgramSqrtWithAdd = question >> LLMRun() >> ExtractCode() >> ((PythonRun(test_case) >> SubstringEvaluator(answer)) & (LLMRun(evaluation) >> SubstringEvaluator("student passes")))

if __name__ == "__main__":
    print(run_test(TestProgramSqrtWithAdd))
