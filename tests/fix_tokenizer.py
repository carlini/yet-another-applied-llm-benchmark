from evaluator import *

DESCRIPTION = "Test if the model can identify and fix an issue with a tokenizer in a Python code snippet. Identifying the problem is in the regex, and fixing the regex, are both hard."

TAGS = ['code', 'fix', 'python']

question = """
Fix this tokenizer keeping it as similar as possible

class Tokenizer:
    def __init__(self, input_str):
        self.tokens = re.findall(r'\d+|(\+|\-|\*|/|sin|cos|\(|\))', input_str)
        self.position = 0

    def get_next_token(self):
        if self.position >= len(self.tokens):
            return None
        token = self.tokens[self.position]
        self.position += 1
        return token

    def peek_next_token(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]
"""

test_case, answer = make_python_test([("Tokenizer('sin(3+2*4)-cos(15)').tokens", "['sin', '(', '3', '+', '2', '*', '4', ')', '-', 'cos', '(', '15', ')']")])


TestSimpleFix = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestSimpleFix))


