import sys
sys.path.append("..")

from evaluator import *
from llm import llm

question = """
Write a python program that prints the string "hello world" and tell me how it works in a sentence
"""

test_case = """
# do nothing
"""

answer = "hello world"


class PrintHello(TestCase):
    def __init__(self, llm):
        self.conversation = Conversation(llm)
        self.evaluate = SubstringEvaluator(answer)
        self.output_processors = [ExtractCode(llm), PythonRun(test_case)]
        self.fix_errors = [RetryFixCodeErrors]

    
print(PrintHello(llm).run(question))
