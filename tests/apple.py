from evaluator import *

DESCRIPTION = "Test if the model can output 10 sentences, ending each one with the word 'apple'."

TAGS = ['explain', 'fun']

question = """
Write a list ten sentences, each of which ends with the word 'apple'.
"""

def test_true():
    return True

import re

def do_split_eos(text):
    for sentence in text.strip().split('\n'):
        if sentence.strip():
            # remove punctuation
            sentence_cleaned = re.sub(r'[^\w\s]$', '', sentence.strip())
            words = sentence_cleaned.split()
            yield words[-1] if words else ""



TestEnding = question >> LLMRun() >> UntilDone(PyEvaluator(test_true), 
(PyFunc(do_split_eos) >> SubstringEvaluator('apple', True)), max_iters=10)

if __name__ == "__main__":
    print(run_test(TestEnding))