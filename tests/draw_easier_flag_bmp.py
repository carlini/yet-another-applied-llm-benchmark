from evaluator import *

TAGS = ['code', 'c', 'visual']

question = """
Write me a C program that emits a .bmp that's a depiction of an italian flag to stdout.
"""

TestEasyFlagDraw = question >> LLMRun() >> ExtractCode(keep_main=True) >> CRun(out_bytes=True) >> LLMVisionRun("What flag is shown in this image?") >> (SubstringEvaluator("Italy") | SubstringEvaluator("Italian"))

if __name__ == "__main__":
    print(run_test(TestEasyFlagDraw))
