from evaluator import *

DESCRIPTION = "Test if the model can understand and interpret a request to gitignore any file called \"foo/.KEYFILE\"  regardless of its location in a repository."

TAGS = ['explain']

question1 = """
gitignore any file called .KEYFILE directly inside a directory foo, which itself is anywhere
"""

TestWhatIsStarStar = question1 >> LLMRun() >> SubstringEvaluator("**/foo/.KEYFILE")

question2 = """
gitignore any file called .KEYFILE anywhere under a directory foo, which itself is anywhere
"""

TestWhatIsStarStarB = question2 >> LLMRun() >> SubstringEvaluator("**/foo/**/.KEYFILE")

if __name__ == "__main__":
    print(run_test(TestWhatIsStarStarB))
