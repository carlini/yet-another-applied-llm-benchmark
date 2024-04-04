from evaluator import *

DESCRIPTION = "Test if the model can infer what data to sum and what to ignore by example with vague instructions."

TAGS = ['code', 'python']

question = '''
Here's some data
QUERY A361
Found at: 160392127418
Number of times present: 4


Found at: 150158692866
Number of times present: 3


Found at: 122340445248
Number of times present: 17


Found at: 137248651778
Number of times present: 84


Found at: 131891981708
Number of times present: 66


QUERY 32B57
Found at: 194561247604
Number of times present: 4


Found at: 82888490886
Number of times present: 3


Found at: 115836535414
Number of times present: 19


Found at: 79615924948
Number of times present: 80

Write a python function called `process` that will take data like this as an argument and return a dict where the keys are the like A361/32B57 and the values are how often its present in total.
'''

data = "QUERY A361\\nFound at: 160392127418\\nNumber of times present: 4\\n\\n\\nFound at: 150158692866\\nNumber of times present: 4\\n\\n\\nFound at: 122340445248\\nNumber of times present: 17\\n\\n\\nFound at: 137248651778\\nNumber of times present: 84\\n\\n\\nFound at: 131891981708\\nNumber of times present: 66\\n\\n\\nQUERY 32B57\\nFound at: 194561247604\\nNumber of times present: 4\\n\\n\\nFound at: 82888490886\\nNumber of times present: 3\\n\\n\\nFound at: 115836535414\\nNumber of times present: 19\\n\\n\\nFound at: 79615924948\\nNumber of times present: 81\\n"

test_case, answer = make_python_test([(f"process('{data}')", "{'A361': 175, '32B57': 107}")])

TestSumSomeData = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestSumSomeData))


