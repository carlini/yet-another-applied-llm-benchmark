from evaluator import *

DESCRIPTION = "Test if a model knows some latex macros explained poorly"

TAGS = ['explain']

question = "Latex format the word METHOD like Method but all caps with the other letters lower"

TextLatexLowerCaps = question >> LLMRun() >> SubstringEvaluator("textsc")

if __name__ == "__main__":
    print(run_test(TextLatexLowerCaps))


