from evaluator import *

DESCRIPTION = "Test if the model can generate a .patch file to fix a bug in a given Python code."

TAGS = ['code', 'fix', 'python']

code = """import re

class Tokenizer:
    def __init__(self, input_str):
        '''
        input_str: a string of digits and operators
        '''
        self.position = 0
        self.tokens = re.findall(r'\d+|(\+|\-|\*|/|sin|cos|\(|\))', input_str)

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

question = f"""
Write a .patch file to stdout that will fix the bug in this tokenizer. Still keep the new file name the same after patching.

I'll evaluate you based on my ability to do
- echo [your patch] > fix.patch
- patch < fix.patch
- python3 run_tokenizer.py



Here is the entirety of run_tokenizer.py:
```python
{code}
```
"""

def setup_fn():
    code = """import re

class Tokenizer:
    def __init__(self, input_str):
        '''
        input_str: a string of digits and operators
        '''
        self.position = 0
        self.tokens = re.findall(r'\d+|(\+|\-|\*|/|sin|cos|\(|\))', input_str)

    def get_next_token(self):
        if self.position >= len(self.tokens):
            return None
        token = self.tokens[self.position]
        self.position += 1
        return token

    def peek_next_token(self):
        if self.position >= len(self.tokens):
            return None
        return self.tokens[self.position]"""
    import time
    open('run_tokenizer.py', 'w').write(code)

    time.sleep(.5)


def check():
    import os
    import time
    os.system("patch < fix.patch")
    time.sleep(.5)
    import run_tokenizer
    return run_tokenizer.Tokenizer("cos(1)+sin(23)*5").tokens == ['cos', '(', '1', ')', '+', 'sin', '(', '23', ')', '*', '5']


TestFixPatch = Setup(setup_fn) >> question >> LLMRun() >> ExtractCode(manual="Take the below answer to my question and return just the complete .patch in a single file so I can copy and paste it into an editor and apply it with the `patch` tool as-is. Include nothing else other than the patch. Here is the code: <A>") >> MakeFile("fix.patch") >> PyEvaluator(check)


if __name__ == "__main__":
    print(run_test(TestFixPatch))
