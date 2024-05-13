from evaluator import *

DESCRIPTION = "This test case checks if the model knows lpr commands."

TAGS = ['explain']

question = """
I have a .ps file that I want to print from my mac. I'm trying to use lpr. But every time I print it all I get is the actual bytes just printed with like hundreds of pages and this is not what I want. I want the printer to just print the ps directly. What command should I use to make this work? 
"""

TestWhatIsLPR = question >> LLMRun() >> (SubstringEvaluator("-o raw") | SubstringEvaluator("-l "))

if __name__ == "__main__":
    print(run_test(TestWhatIsLPR))

