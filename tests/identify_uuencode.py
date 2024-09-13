from evaluator import *

DESCRIPTION = "Test if the model can correctly identify a block of text is uuencoded."

TAGS = ['explain']

question = """
What encoding scheme does it look like this is encoded with?

H,3DR-S<-"C(X,C<U#0HT.3(V-@T*-C`X,C8-"C(X,S8V#0HR,#<Q-0``
"""


TestIsUU = question >> LLMRun() >> SubstringEvaluator("uuencode", lower=True)
    

if __name__ == "__main__":
    print(run_test(TestIsUU))

