from evaluator import *

DESCRIPTION = "Test if the model can interpret vague questions and will respond with the answer I want, not the answer that's easy to find."

TAGS = ['explain']

question = """
What do I do to fix AutoModel.from_pretrained to make it auto model with lm head
"""

TestWhatIsAutoModel = question >> LLMRun() >> SubstringEvaluator("AutoModelForCausalLM")

if __name__ == "__main__":
    print(run_test(TestWhatIsAutoModel))
