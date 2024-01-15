from evaluator import *

DESCRIPTION = "Test if the model can write a Python script that merges a list of file paths into 16 files of approximately equal size."

TAGS = ['code', 'python']

question_easy = """
I have a list of several thousand file paths in /tmp/files. Write a python script that merges these all together and splits the content into 16 files called /tmp/merged_%d for i in 0..15 where each is approximately the same size. To do this, sort files by size (largest first) and add files in order always to the smallest one. "/tmp/files" is a list of file paths, one per line.
"""

question = """
I have a list of several thousand file paths in /tmp/files. Write a python script that merges the content int 16 files called /tmp/merged_%d for i in 0..15 where each is approximately the same size. "/tmp/files" is a list of file paths, one per line.
"""


def setup_fn():
    import random
    import os
    os.mkdir("/tmp/a")
    with open("/tmp/files", "w") as f:
        for i in range(1000):
            f.write("/tmp/a/file_%d\n" % i)
            with open("/tmp/a/file_%d" % i, "w") as f2:
                if i < 5:
                    f2.write("x" * random.randint(10000, 30000))
                else:
                    f2.write("x" * random.randint(1, 1000))
    
def test():
    import os
    import numpy as np
    sz = []
    for i in range(16):
        sz.append(len(open("/tmp/merged_%d" % i).read()))

    size_before = sum(os.path.getsize("/tmp/a/file_%d"%i) for i in range(1000))
    size_after = sum(sz)

    # I ddn't say exactly how to merge, adding newlines is okay
    if abs(size_before-size_after) > 2000:
        return False

    # easy to hit with proper merging, hard otherwise
    # 10 trials suggest the range is usualy [10, 40]
    return max(sz) - min(sz) < 200
            
                    
    
TestMake16FilesEasy = Setup(setup_fn) >> question_easy >> LLMRun() >> ExtractCode(keep_main=True) >> Echo() >> PythonRun() >> PyEvaluator(test)

TestMake16Files = Setup(setup_fn) >> question >> LLMRun() >> ExtractCode(keep_main=True) >> Echo() >> PythonRun() >> PyEvaluator(test)


if __name__ == "__main__":
    print(run_test(TestMake16FilesEasy))
