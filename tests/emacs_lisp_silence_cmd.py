from evaluator import *

question = """
In emacs lisp how do I silence "Process python-process finished"
"""

TestLispSilencePython = question >> LLMRun() >> SubstringEvaluator("set-process-sentinel")


if __name__ == "__main__":
    print(run_test(TestLispSilencePython))
