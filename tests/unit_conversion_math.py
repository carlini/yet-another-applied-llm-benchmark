from evaluator import *

DESCRIPTION = "Test if a model can do basic math with some EE equations."

TAGS = ['explain']

question = "I measure a voltage drop of 30mv over a 2.5 ohm resistor. How long will a 3Ah battery last? Write your ansser 'XXX hours'"

TestUnitConversion = question >> LLMRun() >> RegexEvaluator("250.{,10}hours")

if __name__ == "__main__":
    print(run_test(TestUnitConversion))


