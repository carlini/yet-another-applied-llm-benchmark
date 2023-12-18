import sys
sys.path.append("..")

from evaluator import *
from llm import llm

question = """
Tell me how to compute sqrt() in python without using the sqrt() function, then give me a function to do this. I want the answer as precise as possible. Call the function my_sqrt().
"""

test_case, answer = make_python_test([("round(my_sqrt(12345), 1)", "111.1")])


class ProgramSqrt(TestCase):
    def __init__(self, llm):
        self.conversation = Conversation(llm)
        self.evaluate = SubstringEvaluator(answer)
        self.output_processors = [ExtractCode(llm), PythonRun(test_case)]
        self.fix_errors = [RetryFixCodeErrors]

    
print(ProgramSqrt(llm).run(question))
