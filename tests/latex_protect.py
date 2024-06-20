from evaluator import *

DESCRIPTION = "Test if a model can fix a latex newline error in a caption"

TAGS = ['explain']

question = r"""
In latex when I force a newline in a caption with \\  it gives an error saying \Hy@tempa has an extra } runaway argument?
"""

# \newline doesn't work the same I need \\
TestLatexNewline = question >> LLMRun() >> SubstringEvaluator("\\protect")

if __name__ == "__main__":
    print(run_test(TestLatexNewline))
