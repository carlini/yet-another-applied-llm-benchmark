import sys
sys.path.append("..")

from evaluator import *
from llm import llm

question = """
I'm making pancakes for breakfast. I added a cup of flour, a teaspoon of salt, and a few tablespoons of sugar to a bowl. I stirred it together, then added a cup of milk, a beaten egg, and a few tablespoons of oil, and stirred until just mixed. Then I put 1/4 a cup on a hot frying pan, and flipped it when brown. But they're terrible! Why? List one reason.
"""

evaluation = """
Below is a student's answer to a question on what is missing from some pancake recipe: <A>

Does the student mention that baking powder or baking soda is missing? Begin your answer with Yes or No. and then justify why.
"""


class PrintHello(TestCase):
    def __init__(self, llm):
        self.conversation = Conversation(llm)
        self.evaluate = LLMEvaluator(llm, evaluation)
        self.output_processors = []
        self.fix_errors = []
    
    
print(PrintHello(llm).run(question))
