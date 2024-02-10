from evaluator import *

DESCRIPTION = "Test if the model can rewrite a very simple Python program into an equivalent C program."

TAGS = ['code', 'c']

question = """
Here's a python program. Please rewrite it in c with the type signature float my_sqrt(float, float).

def my_sqrt(number, precision=0.0001):
    guess = number / 2  # Start with an initial guess
    
    while abs(guess * guess - number) >= precision:
        guess = (guess + number / guess) / 2  # Improve the guess using the Babylonian method
    
    return guess
"""

test_case, answer = make_c_test([("(int)(my_sqrt(12345, .001)*10)", "1111")])


TestProgramRewriteCSimple = question >> LLMRun() >> ExtractCode() >> CRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    from llm import llm
    print(run_test(TestProgramRewriteCSimple))
