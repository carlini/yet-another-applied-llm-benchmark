from evaluator import *

DESCRIPTION = "Test if the model can identify the buf and fix a program that handles python tracebacks. Useful to know if the model can handle more advanced python libraries."

TAGS = ['code', 'fix']

question = """
Fix this program. Make sure to keep the format "var: value".

import traceback

def foo():
    y = 6
    raise Exception("This is a test exception")

def crashes():
    x = 5
    foo()


if __name__ == "__main__":
    try:
        crashes()
    except:
        # extract stack frames                                                                                                                                                        
        stack = traceback.extract_stack()
        # print all locals in each stack frame
        for frame in stack:
            for k,v  in frame.locals:
                print(k + ": " + v)
"""

TestProgramTB = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun("") >> (SubstringEvaluator("x: 5") & SubstringEvaluator("y: 6"))

if __name__ == "__main__":
    print(run_test(TestProgramTB))
