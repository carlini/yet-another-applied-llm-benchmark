from evaluator import *

DESCRIPTION = "Test if the model can identify a missing incredient in a recipe. Identifying incorrect steps is much harder than missing steps."

TAGS = ['explain', 'fun']

question = """
I'm making pancakes for breakfast. I added a cup of flour, a teaspoon of salt, and a few tablespoons of sugar to a bowl. I stirred it together, then added a cup of milk, a beaten egg, and a few tablespoons of oil, and stirred until just mixed. Then I put 1/4 a cup on a hot frying pan, and flipped it when brown. But they're terrible! Why? List the main reason.
"""

evaluation = """
Below is a student's answer to a question on what is missing from some pancake recipe: <A>

Does the student mention that baking powder or baking soda is missing? Think out loud, and then end your answer with either the string "The student passes" or "The student fails".
"""

TestMissingStep = question >> LLMRun() >> LLMRun(evaluation, llm=EVAL_LLM) >> SubstringEvaluator("student passes")
    

if __name__ == "__main__":
    print(run_test(TestMissingStep))
