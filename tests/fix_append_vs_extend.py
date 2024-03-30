from evaluator import *

DESCRIPTION = "This test checks is the model can figure out from context when it's right to use extend versus append."

TAGS = ['explain', 'python']

question = """
Why won't this function work as expected? List exactly one reason.

```
def make_op_with_history(config):
    how = config[0]
    args = config[1:]

    if how.split()[0] == 'dot_from_papers':
        return [(how, make_op(config))]
    if how.split()[0] in ['const_add', 'const_mul']:
        return [(how, make_op(config))] + make_op_with_history(config[1])
    out = []
    for arg in args:
        hist = make_op_with_history(arg)
        out.append(hist)
    return [(how, make_op(config))] + out
```
"""

judge = "I asked a question about why some code was incorrect. The answer is \"because because the code uses append instead of extend\". Does this student answer say that? Giving multiple answers is okay as long as it also says somewhere that the code should replace the append with extend.\n\n<A>\n\nAnswer either 'The student passes' or 'The student fails'."

TestAppendNotExtend = question >> LLMRun() >> (LLMRun(judge, llm=EVAL_LLM) >> SubstringEvaluator("student passes"))

if __name__ == "__main__":
    print(run_test(TestAppendNotExtend))


