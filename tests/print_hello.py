from evaluator import *

DESCRIPTION = "Test if the model can generate a basic python program that prints \"hello world\"."

TAGS = ['code', 'python']

question = 'Write a python program that prints the string "hello world" and tell me how it works in a sentence'

answer = "hello world"

TestPrintHello = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestPrintHello))

