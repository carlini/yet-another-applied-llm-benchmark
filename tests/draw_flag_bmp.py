from evaluator import *

DESCRIPTION = "Test if the model can write a C program that draws an image. This test requires the ability to understand the .bmp specification, and draw a flag that can be correctly parsed and seen by the evaluator."

TAGS = ['code', 'c', 'visual']

question = """
Write me a C program that emits a .bmp that's a depiction of an american flag to stdout.
"""

TestFlagDrawBMP = question >> LLMRun() >> ExtractCode(keep_main=True) >> CRun(out_bytes=True) >> LLMVisionRun("What flag is shown in this image?") >> (SubstringEvaluator("United States") | SubstringEvaluator("USA") | SubstringEvaluator("America"))


question2 = """
Write me a C program that emits a .bmp that's a depiction of an italian flag to stdout.
"""

TestEasyFlagDrawBMP = question2 >> LLMRun() >> ExtractCode(keep_main=True) >> CRun(out_bytes=True) >> LLMVisionRun("What flag is shown in this image?") >> (SubstringEvaluator("Italy") | SubstringEvaluator("Italian"))


if __name__ == "__main__":
    print(run_test(TestFlagDrawBMP))
