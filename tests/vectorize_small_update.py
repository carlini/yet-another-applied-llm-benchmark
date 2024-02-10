from evaluator import *

DESCRIPTION = "Test if the model can replace a for loop with a vectorized version."

TAGS = ['code', 'python', 'performance']

def update(high, highest_number, delta):
    for i in range(len(high)):
        if i != highest_number:
            high[i] = min(high[i], high[highest_number] + delta[highest_number] - delta[i])
    return high

question = """
Vectorize this update loop. Call the function `update`:

import numpy as np

def update(high, highest_number, delta):
    for i in range(len(high)):
        if i != highest_number:
            high[i] = min(high[i], high[highest_number] + delta[highest_number] - delta[i])
    return high
"""

test_case, answer = make_python_test([("list(update(np.array([2, 5, 9, 1, 2, 0, 3, 8]), 4, np.array([1, 2, 1, 4, 3, 2, 1, 2])))", "[2, 3, 4, 1, 2, 0, 3, 3]")], header="import numpy as np")

evaluation = """
Below is a student's answer to a question about how to vectorize this loop:

def update(high, highest_number, delta):
    for i in range(len(high)):
        if i != highest_number:
            high[i] = min(high[i], high[highest_number] + delta[highest_number] - delta[i])
    return high

Here is their code:

<A>

Did the student try to vectorize the loop? Don't tell me if they are correct or not. (I have tests for that separately which will catch any bugs.) Just tell me if they tried to vectorize the loop. End your answer with either the string "The student passes" if they tried to do a vectorized loop, or "The student fails" if they just wrote a for loop again.
"""

TestVectorizeSmall = question >> LLMRun() >> ExtractCode() >> ((PythonRun(test_case) >> SubstringEvaluator(answer)) & (LLMRun(evaluation) >> SubstringEvaluator("student passes")))

if __name__ == "__main__":
    print(run_test(TestVectorizeSmall))
