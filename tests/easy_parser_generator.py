from evaluator import *

DESCRIPTION = "Test if the model can understand a vague BNF-style grammar and write a Python function that evaluates expressions based on the grammar rules."

TAGS = ['code', 'python']

question = """
Given this BNF-style grammar write a Python function `evaluate(str)` that evaluates the expression

<expression> ::= <term> | <expression> '+' <term> | <expression> '-' <term>

<term> ::= <factor> | <term> '*' <factor> | <term> '/' <factor>

<factor> ::= <number> | '(' <expression> ')' | <prefix-op> <factor>

<prefix-op> ::= 'sin' | 'cos'

<number> ::= <digit> | <number> <digit>

<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

For example you can evaluate this

sin(3 + 2 * 4) - cos(15) = -0.240302
"""

test_case, answer = make_python_test([("round(evaluate('sin(35+2*4)-cos(15)'), 5)", "-0.07209")])

TestSimpleBNF = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestSimpleBNF))


