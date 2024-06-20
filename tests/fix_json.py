from evaluator import *

DESCRIPTION = "Test if the model can fix broken JSON objects."

TAGS = ['code', 'python']

question = """Write me a python function called fix_json that fixes broken JSON objects, and returns the parsed object. I'll pass the JSON object as a string and it should fix:
- Incorect parenthesis, e.g., {"a": (5, 4)} -> {"a": [5, 4]}
- Incorrect single quotes, e.g., {'a': 5} -> {"a": 5}
- False/True -> false/true
"""

help_err = """Make sure not to break data inside strings! So if there's a True or a ( inside a string keep them the way they are. Also don't break quoted strings"""

test_case, answer = make_python_test([("""fix_json('''{"a": 5, "b": [3, 4]}''')""", """{"a": 5, "b": [3, 4]}"""),
                                      ("""fix_json('''{'a': 5.0, 'b': (True, 4)}''')""", """{"a": 5.0, "b": [True, 4]}"""),
                                      ("""fix_json('''{'True': False, 'b()': (3, 4), "c'": []}''')""", """{"True": False, "b()": [3, 4], "c'": []}"""),
                                      ])

TestFixJSON = question >> LLMRun() >> ExtractCode(keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)
TestFixJSONHelp = (question+help_err) >> LLMRun() >> ExtractCode(keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestFixJSONHelp))

