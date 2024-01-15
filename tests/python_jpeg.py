from evaluator import *

DESCRIPTION = "Test if a model can write a program that directly writes a jpeg file. This requires precise understanding of the jpeg spec."

TAGS = ['code', 'python', 'visual']

question = """
Write a python program that, manually, draws a red triangle on a white background and saves it as a 200x200 gif file. Do not use any graphics libraries. Write the gif byte by byte. Output the gif file to stdout.

I will evaluate your program by running `python your_soln.py > /tmp/a.gif` and then view the output file.
"""

TestFlagDraw = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun(out_bytes=True) >> LLMVisionRun("Describe the shapes in this image and their color") >> (SubstringEvaluator("triangle") & SubstringEvaluator("red"))

if __name__ == "__main__":
    print(run_test(TestFlagDraw))
