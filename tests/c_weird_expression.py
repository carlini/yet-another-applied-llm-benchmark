from evaluator import *

TAGS = ['explain', 'c']

question = """
What does the c expression `-~++*x--` evaluate to in simplest form? Ignore side effects. Think out loud then give a final summary.
"""

evaluation = """
Below is a student's answer to a question about what a particular C expression evaluates to: <A>

Does the student's final answer say that the expression evaluates to *x+2?

Ignore their reasoning. Just look at the final answer, if they say **EXPLICITLY** that the answer is *x+2. Giving something that's equal but more complicated is wrong. 

If the answer is correct say "The student passes" otherwise "The student fails".
"""

TestExplainWeirdC = question >> LLMRun() >> LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")
    

if __name__ == "__main__":
    print(run_test(TestExplainWeirdC))
