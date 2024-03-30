from evaluator import *


DESCRIPTION = "Test if the model can create a tree from a string."

TAGS = ['code', 'python']

code = """
class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        if parent:
            self.parent.children.append(self)
    def __repr__(self):
        if self.children == []:
            return self.name
        return '('+self.name + ' ' + ' '.join(repr(c) for c in self.children)+')'
"""

question = code + """

Write a complete python file that will print the tree

(1 (2 3) 4)

Call the root of the tree 'root'.
Then print out str(root).
DO NOT MODIFY THE Node CLASS.
"""

TestMakeTreeEasy = question >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> SubstringEvaluator('(1 (2 3) 4)')

question2 = code + """

Write a complete python file that will print the tree

(1 (2 (3 4 5 6) (7 8)) (9 10 (11 12)))

Call the root of the tree 'root'.
Then print out str(root).
"""

TestMakeTree = question2 >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> SubstringEvaluator('(1 (2 (3 4 5 6) (7 8)) (9 10 (11 12)))')


if __name__ == "__main__":
    print(run_test(TestMakeTreeEasy))
