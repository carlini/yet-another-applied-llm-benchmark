from evaluator import *

DESCRIPTION = "Test if the model can implement a sqrt function."

TAGS = ['code', 'python']

question = """
Tell me how to compute sqrt() in python without using the sqrt() function, then give me a function to do this. I want the answer as precise as possible. Call the function my_sqrt()..
"""

test_case, answer = make_python_test([("round(my_sqrt(12345), 1)", "111.1")])


TestProgramSqrt = question >> LLMRun() >> ExtractCode() >> ((LLMRun("Below is a student question who was supposed to implement square root from scratch. Did they cheat and just call sqrt directly? Think out loud, then finally answer either 'Yes they cheated' or 'No they did not cheat' <A>", llm=EVAL_LLM) >> ~SubstringEvaluator("they cheated")) & (PythonRun(test_case) >> SubstringEvaluator(answer)))
    
    
if __name__ == "__main__":
    print(run_test(TestProgramSqrt))

