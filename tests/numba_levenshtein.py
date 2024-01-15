from evaluator import *

DESCRIPTION = "Test if the model can generate a numba implementation of the Levenshtein distance algorithm."

TAGS = ['code', 'python', 'performance']

question = """
Write me a numba implementation of levensthin distance, taking two numpy int arrays. Call it levenshtein. Run it in nopython mode. Character swaps are cost 2.
"""

test_case, answer = make_python_test([("levenshtein(np.array([3, 5, 2, 4, 8, 7]), np.array([3, 4, 2, 4, 8, 7, 9]))", "3")])


TestProgramNumbaLev = question >> LLMRun() >> ExtractCode(keep_main=False) >> (((SubstringEvaluator("from numba") | SubstringEvaluator("import numba")) & (SubstringEvaluator("nopython") | SubstringEvaluator("njit"))) & PythonRun(test_case) >> SubstringEvaluator(answer))

if __name__ == "__main__":
    print(run_test(TestProgramNumbaLev))
