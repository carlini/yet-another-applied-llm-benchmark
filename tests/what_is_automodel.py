from evaluator import *

question = """
What do I do to fix AutoModel.from_pretrained to make it auto model with lm head
"""

TestWhatIsAutoModel = question >> LLMRun() >> SubstringEvaluator("AutoModelForCausalLM")

if __name__ == "__main__":
    print(run_test(TestWhatIsAutoModel))
