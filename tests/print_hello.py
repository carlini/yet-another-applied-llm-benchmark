from evaluator import *

question = 'Write a python program that prints the string "hello world" and tell me how it works in a sentence'

answer = "hello world"

TestPrintHello = question >> LLMRun() >> ExtractCode() >> PythonRun() >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestPrintHello))

