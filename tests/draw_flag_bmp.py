from evaluator import *

question = """
Write me a C program that emits a .bmp that's a depiction of an american flag to stdout.
"""

TestFlagDraw = question >> LLMRun() >> ExtractCode(keep_main=True) >> CRun(out_bytes=True) >> LLMVisionRun("What flag is shown in this image?") >> (SubstringEvaluator("United States") | SubstringEvaluator("USA") | SubstringEvaluator("America"))

if __name__ == "__main__":
    print(run_test(TestFlagDraw))
