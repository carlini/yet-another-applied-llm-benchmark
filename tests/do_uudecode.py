from evaluator import *

DESCRIPTION = "Test if the model can successfully uudecode a given string."

TAGS = ['explain']

question = """
uudecode this string:

H,3DR-S<-"C(X,C<U#0HT.3(V-@T*-C`X,C8-"C(X,S8V#0HR,#<Q-0``
"""


TestUUDecode = question >> LLMRun() >> (SubstringEvaluator("60826") & SubstringEvaluator("20715") & SubstringEvaluator("19277"))
    

if __name__ == "__main__":
    print(run_test(TestUUDecode))

