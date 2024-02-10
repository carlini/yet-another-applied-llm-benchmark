from evaluator import *

DESCRIPTION = "Test if the model can understand a DP algorithm and then convert it into an iterative implementation."

TAGS = ['code', 'performance', 'python']

my_code = """
@lru_cache(maxsize=None)
def solve_dp(graph, lines_left, distance_since_last):
    if len(graph) < lines_left: return 1e9, []
    if lines_left == 0 and len(graph) == 0: return 0, []

    # option 1: don't take the line
    value = (1e9, [])
    if distance_since_last < 10:
        value = min(value, solve_dp(graph[1:], lines_left, distance_since_last+1))

    # option 2: take the line
    if lines_left > 0:
        sub, how = solve_dp(graph[1:], lines_left-1, 0)
        sub += graph[0] + (distance_since_last-8)**2
        value = min(value, (sub, how + [len(graph)]))

    return value
"""

question = f"""
Explain what this code does. Then, convert this recursive function to an iterative one, making explicit the cubic work that's being done. The functions should return exactly the same output but the iterative one should be faster. Call your function `solve_iterative` and match the type signature of the original function.

{my_code}
"""

test_case, answer = make_python_test([(f"""0
import random
mylist = list(range(100))
random.shuffle(mylist)
from functools import lru_cache

{my_code.replace("solve_dp", "my_solve_dp")}
answer = solve_iterative(tuple(mylist), len(mylist)//8, 4)""",
                                       "my_solve_dp(tuple(mylist), len(mylist)//8, 4)")])

def not_recursive(code):
    return code.count("solve_iterative") == 1, ""

TestProgramRemoveDP = question >> LLMRun() >> ExtractCode() >> \
    (PyFunc(not_recursive) & (PythonRun(test_case) >> SubstringEvaluator(answer)))

if __name__ == "__main__":
    print(run_test(TestProgramRemoveDP))
