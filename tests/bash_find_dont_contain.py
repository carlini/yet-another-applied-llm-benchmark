from evaluator import *

DESCRIPTION = "Test if a model can implement (the negation of) a simple bash 1-liner searching for files that don't contain some text."

TAGS = ['bash']

question = "In bash list all files in cwd that don't contain asdf in the contents (case-ignore)"


def setup_fn():
    open("hello", "w").write("this is a test")
    open("there", "w").write("test this ASDF")
    open("this", "w").write("whatever thing")
    open("asdf", "w").write("zzzthing")
    open("lower", "w").write("test this asdf")

    
TestBashFindDontContain = Setup(setup_fn) >> question >> LLMRun() >> ExtractCode(keep_main=True) >> BashRun() >> (SubstringEvaluator("hello") & ~SubstringEvaluator("there") & SubstringEvaluator("this") & SubstringEvaluator("asdf") & ~SubstringEvaluator("lower"))


if __name__ == "__main__":
    print(run_test(TestBashFindDontContain))

