from evaluator import *

DESCRIPTION = "This test case is meant to test if the model can correctly evaluate a complex C expression."

TAGS = ['explain', 'c']


evaluation = """
Below is a student's answer to a question about what a particular C expression evaluates to: <A>

Does the student's final answer say that the expression evaluates to *x+2?

Ignore their reasoning. Just look at the final answer, if they say **EXPLICITLY** that the answer is *x+2. Giving something that's equal but more complicated is wrong. 

If the answer is correct say "The student passes" otherwise "The student fails".
"""


question = """
What does the c expression `-~++*x--` evaluate to in simplest form? Ignore side effects. Think out loud then give a final summary.
"""

TestExplainWeirdCEasy = question >> LLMRun() >> LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")

question_harder = """
What does the c expression `-~++*x--` evaluate to in simplest form? Ignore side effects.
"""

TestExplainWeirdC = question_harder >> LLMRun() >> LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")


if __name__ == "__main__":
    print(run_test(TestExplainWeirdC))
