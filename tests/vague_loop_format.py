from evaluator import *

DESCRIPTION = "Test if the model can follow vague instructions for how to print IDs following an example."

TAGS = ['code', 'python']

question = """
Write a python program that for ids like

2401_002

For months 1..12 and ids 1..3

so like 24{month}_{id}

print all the ids
"""

evaluator = SubstringEvaluator("2401_001")
for month in range(1, 13):
    for id in range(1, 4):
        evaluator &= SubstringEvaluator(f"24{month:02}_{id:03}")


TestVagueLoopFormat = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> evaluator


if __name__ == "__main__":
    print(run_test(TestVagueLoopFormat))


