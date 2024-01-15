from evaluator import *

DESCRIPTION = "Test if the model can parallelize a python program to perform a wordcount."

TAGS = ['code', 'python', 'performance']
import collections

question = """
Write a self-contained Python program that prints a JSON output of how often each word appears in a text file located in /tmp/file.txt. So if the file contains "This is is is, an example" then the program should print to stdout.

{"This": 1, "is": 2, "is,":1, "an":1, "example":1}

The program should be run by calling /path/to/python_word_count with no arguments.

Make it run in parallel on 4 cores at the same time, each taking 1/4 of the file.
Print out 4 differnt json dicts, one per line. I'll do the merging.
"""



def setup():
    txt = "it was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we had nothing before us, we were all going direct to Heaven, we were all going direct the other way"    
    open("/tmp/file.txt", "w").write(txt)
    

def merge(dicts):
    out = {}
    for line in dicts.split("\n"):
        if line:
            if '{' not in line: continue
            try:
                d = json.loads(line)
            except:
                continue
            for k, v in d.items():
                out[k] = out.get(k, 0) + v
    return out
    
TestPythonCountPar = Setup(setup) >> StringNode(question) >> LLMRun() >> ExtractCode(keep_main=True) >> ((PythonRun() >> PyFunc(merge) >> EqualEvaluator(({'the': 11, 'it': 10, 'was': 10, 'of': 10, 'we': 4, 'times,': 2, 'age': 2, 'epoch': 2, 'season': 2, 'had': 2, 'before': 2, 'us,': 2, 'were': 2, 'all': 2, 'going': 2, 'direct': 2, 'best': 1, 'worst': 1, 'wisdom,': 1, 'foolishness,': 1, 'belief,': 1, 'incredulity,': 1, 'Light,': 1, 'Darkness,': 1, 'spring': 1, 'hope,': 1, 'winter': 1, 'despair,': 1, 'everything': 1, 'nothing': 1, 'to': 1, 'Heaven,': 1, 'other': 1, 'way': 1}))) & (LLMRun("Below is some student's code. I asked them to parallelize some code. Do not judge if it is correct, I have test cases for that. Just tell me if they tried to parallelize it.\n\n<A>\n\nAnswer either 'The student passes' or 'The student fails'.", llm=EVAL_LLM) >> Echo() >> SubstringEvaluator("student passes")))


if __name__ == "__main__":
    print(run_test(TestPythonCountPar))
