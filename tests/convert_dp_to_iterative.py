import sys
sys.path.append("..")

from evaluator import *
from llm import llm

my_code = """
@lru_cache(maxsize=None)
def solve_dp(graph, lines_left, distance_since_last=4):
    if len(graph) < lines_left: return 1e9, []
    if lines_left == 0 and len(graph) == 0: return 0, []

    # option 1: don't take the line                                                                                                                                               
    value = (1e9, [])
    if distance_since_last < 10:
        value = min(value, solve_dp(graph[1:], lines_left, distance_since_last+1))

    # option 1: take the line                                                                                                                                                     
    if lines_left > 0:
        sub, how = solve_dp(graph[1:], lines_left-1, 0)
        sub += graph[0] + (distance_since_last-8)**2
        value = min(value, (sub, how + [len(graph)]))

    return value
"""

question = f"""
Explain what this code does. Then, convert this recursive function to an iterative one, making explicit the cubic work that's being done. The functions should return exactly the same output but the iterative one should be faster. Call your function `solve_iterative`

{my_code}
"""

test_case, answer = make_python_test([(f"""0
import random
mylist = list(range(100))
random.shuffle(mylist)
from functools import lru_cache

{my_code}
answer = solve_iterative(mylist, len(mylist)//8, 4)""",
                                       "solve_dp(tuple(mylist), len(mylist)//8, 4)")])


class ProgramRemoveDP(TestCase):
    def __init__(self, llm):
        self.conversation = Conversation(llm)
        self.evaluate = SubstringEvaluator(answer)
        self.output_processors = [ExtractCode(llm), PythonRun(test_case)]
        self.fix_errors = [] # RetryFixCodeErrors

    
print(ProgramRemoveDP(llm).run(question))
