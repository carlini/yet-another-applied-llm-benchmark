from evaluator import *

DESCRIPTION = "Test if the model can write a bash script that renames files with a specific pattern."

TAGS = ['code', 'bash']

question = """
Write a bash script to rename all files of the form "merged_*" to "finished_*". I want to call it by running bash rename.sh /path/to/files.
"""

def setup_fn():
    import os
    import time
    os.mkdir("./foo")
    time.sleep(.5)
 
    for i in range(10):
        with open("./foo/merged_{}".format(i), "w") as f:
            f.write("a"*i)
        with open("./foo/{}".format(i), "w") as f:
            f.write("a"*i)

    time.sleep(.5)

def check_ok():
    import os
    return sorted(os.listdir("foo")) == sorted(["finished_{}".format(i) for i in range(10)] + [str(i) for i in range(10)])
    


TestBashRenamer = Setup(setup_fn) >> question >> LLMRun() >> ExtractCode() >> BashRun(args=["foo/"]) >> PyEvaluator(check_ok)

if __name__ == "__main__":
    print(run_test(TestBashRenamer))

