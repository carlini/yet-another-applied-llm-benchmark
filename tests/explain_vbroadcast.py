from evaluator import *

TAGS = ['explain']

question = """
What does the VPBROADCASTB instruction do?
"""

evaluation = """
Below is a student's answer to a question about what a particular C expression evaluates to: <A>

Does the student's say something similar to "Load integer data from the source operand (the second operand) and broadcast to all elements of the destination operand (the first operand)."?

If the answer is correct say "The student passes" otherwise "The student fails".
"""

TestExplainBroadcast = question >> LLMRun() >> LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")
    

if __name__ == "__main__":
    print(run_test(TestExplainBroadcast))
