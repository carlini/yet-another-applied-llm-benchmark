from evaluator import *

DESCRIPTION = "Test if the model can optimize a given Python program for speed and memory efficiency."

TAGS = ['code', 'performance', 'python']

question = """
I have this program

import numpy as np
def diff(out, templates):
    return (out[:, None, :] - templates[None, :, :]).square().sum(2)

Make it faster and more memory efficient without expanding the arrays. Call it `diff` still.
"""

tracer = """
import tracemalloc
import numpy as np

if __name__ == "__main__":
    tracemalloc.start()  # Start tracing

    snapshot1 = tracemalloc.take_snapshot()  # Before execution
    diff(np.arange(10000).reshape((100, 100)), np.arange(10000).reshape((100, 100)))
    snapshot2 = tracemalloc.take_snapshot()  # After execution

    # Calculate the difference in memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()  # Stop tracing

    if peak < 10**6:
        print("Efficient")
"""

test_case, answer = make_python_test([("diff(np.arange(100).reshape((10, 10)), np.arange(100).reshape((10, 10))).sum()", "1650000")])


TestFastL2 = question >> LLMRun() >> ExtractCode() >> \
          ((PythonRun(test_case) >> SubstringEvaluator(answer)) &
           (PythonRun(tracer) >> SubstringEvaluator("Efficient")) &
           (LLMRun("Below is a students answer to a question on writing efficient code. They're supposed to be vectorizing a loop. Is the following code vectorized? It is incorrect to use for loops explicitly. Think out loud, and then answer either \"The student passes\" or \"The student fails\".\n<A>", llm=EVAL_LLM) >> SubstringEvaluator("student passes")))
                                                                    

if __name__ == "__main__":
    print(run_test(TestFastL2))
