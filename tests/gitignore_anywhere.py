from evaluator import *

DESCRIPTION = "Test if the model can understand and interpret a request to gitignore any file called \".KEYFILE\" regardless of its location in a repository."

TAGS = ['explain']

question = """
gitignore any file called .KEYFILE anywhere
"""

TestWhatIsStarStar = question >> LLMRun() >> SubstringEvaluator("**/.KEYFILE")

if __name__ == "__main__":
    print(run_test(TestWhatIsStarStar))
