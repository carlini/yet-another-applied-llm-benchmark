from evaluator import *

DESCRIPTION = "Test if a model can use latex \\renewcommand, and do a bit more than what I actually asked."

TAGS = ['explain']

question = """
Redfine \\paragraph to be \\bigskip\\textbf
"""

TestLatexRedef = question >> LLMRun() >> ((SubstringEvaluator("\\renewcommand{\\paragraph}") | SubstringEvaluator("\\renewcommand\\paragraph")) & SubstringEvaluator("\\bigskip") & SubstringEvaluator("\\textbf") & SubstringEvaluator("\\noindent"))

if __name__ == "__main__":
    print(run_test(TestLatexRedef))
