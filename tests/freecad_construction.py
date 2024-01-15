from evaluator import *

DESCRIPTION = "Test if the model understands a rambling question about how to make construction circle in FreeCAD."

TAGS = ['explain', 'fun']

question = """
In freecad I want to have a circle but only like for reference not to actually be a circle but just so I can line up other lines to make a hexagon for example, how do I do that
"""

TestFreeCADCircle = question >> LLMRun() >> (SubstringEvaluator("construction geometry") | SubstringEvaluator("construction circle"))
    

if __name__ == "__main__":
    print(run_test(TestFreeCADCircle))
