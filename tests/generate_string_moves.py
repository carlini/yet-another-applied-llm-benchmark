from evaluator import *

DESCRIPTION = "Test if the model can write code to perform string slicing with vague instructions."

TAGS = ['code', 'python']

question = """
Write me a function called `move` that, given a string x, returns all possible alternate strings y' such that y' is derived from x by moving a substring of x to an arbitrary position
"""


test_case, answer = make_python_test([("set(move('abcdef'))", "set(['abcdef', 'abcdfe', 'abcedf', 'abcefd', 'abcfde', 'abdcef', 'abdecf', 'abdefc', 'abecdf', 'abefcd', 'abfcde', 'acbdef', 'acdbef', 'acdebf', 'acdefb', 'adbcef', 'adebcf', 'adefbc', 'aebcdf', 'aefbcd', 'afbcde', 'bacdef', 'bcadef', 'bcdaef', 'bcdeaf', 'bcdefa', 'cabdef', 'cdabef', 'cdeabf', 'cdefab', 'dabcef', 'deabcf', 'defabc', 'eabcdf', 'efabcd', 'fabcde'])")])

TestProgramStringSlice = question >> LLMRun() >> ExtractCode() >> PythonRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestProgramStringSlice))

