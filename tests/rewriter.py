from evaluator import *

prompt = '''
You are going to refactor some code for me. I have modified the way to call the functions. Here are three examples of how to do a refactor:

Example Case 1:

INPUT:
```
from evaluator import *

question = """
Write a python program that prints the string "hello world" and tell me how it works in a sentence
"""

answer = "hello world"


class PrintHello(TestCase):
    fix_errors = RetryFixCodeErrors
    def setup(self):
        return ExtractCode(self.llm, keep_main=False) >> SubstringEvaluator(answer)

    
if __name__ == "__main__":
    from llm import llm, eval_llm
    print(PrintHello(llm).run(question))
```

OUTPUT:
```
from evaluator import *

question = 'Write a python program that prints the string "hello world" and tell me how it works in a sentence'

answer = "hello world"

TestPrintHello = question >> LLMRun() >> ExtractCode() >> PythonRun() >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestPrintHello))
```

Example Case 2:

INPUT:
```
from evaluator import *

question = """
Disassemble the following python into a function called foo:

  5           0 BUILD_LIST               0
              2 STORE_FAST               1 (primes)

  6           4 LOAD_GLOBAL              0 (range)
              6 LOAD_CONST               1 (2)
              8 LOAD_FAST                0 (max_number)
             10 LOAD_CONST               2 (1)
             12 BINARY_ADD
             14 CALL_FUNCTION            2
             16 GET_ITER
        >>   18 FOR_ITER                94 (to 114)
             20 STORE_FAST               2 (possible_prime)
"""

test_case, answer = make_python_test([("foo(20)", "[2, 3, -3, 5, -5, 7, -7, 11, -11, 13, -13, 17, -17, 19, -19]")])

class Disas1(TestCase):
    def setup(self):
        return ExtractCode(self.llm, keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    from llm import llm
    print(Disas1(llm).run(question))
```

OUTPUT:
```
from evaluator import *

question = """
Disassemble the following python into a function called foo:

  5           0 BUILD_LIST               0
              2 STORE_FAST               1 (primes)

  6           4 LOAD_GLOBAL              0 (range)
              6 LOAD_CONST               1 (2)
              8 LOAD_FAST                0 (max_number)
             10 LOAD_CONST               2 (1)
             12 BINARY_ADD
             14 CALL_FUNCTION            2
             16 GET_ITER
        >>   18 FOR_ITER                94 (to 114)
             20 STORE_FAST               2 (possible_prime)
"""

test_case, answer = make_python_test([("foo(20)", "[2, 3, -3, 5, -5, 7, -7, 11, -11, 13, -13, 17, -17, 19, -19]")])

TestDisas1 = question >> LLMRun() >> ExtractCode(keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestDisas1))
```

Example Case 3:

INPUT:
```
from evaluator import *

question = """
Draw an image of a house with a chimney using WebGL in a single HTML file. Make the canvas take the full page.
"""

class DrawTriangle(TestCase):
    def setup(self):
        return ExtractCode(self.llm, keep_main=False) >> SeleniumDraw() >> LLMVisionRun(self.vision_eval_llm, "What object is drawn in this image?", "/tmp/a.png") >> LLMRun(self.eval_llm, "Does this answer say that there is a picture of a house with a chimney \"<A>\"? Answer \"Yes it does\" or \"No it does not\".") >> SubstringEvaluator("es it does")

if __name__ == "__main__":
    from llm import llm, eval_llm, vision_eval_llm
    print(DrawTriangle(eval_llm, eval_llm=eval_llm, vision_eval_llm=vision_eval_llm).run(question))
```

OUTPUT:
```
from evaluator import *

question = """
Draw an image of a house with a chimney using WebGL in a single HTML file. Make the canvas take the full page.
"""

TestDrawTriangle = question >> LLMRun() >> ExtractCode(keep_main=False) >> SeleniumDraw() >> LLMVisionRun("What object is drawn in this image?") >> LLMRun("Does this answer say that there is a picture of a house with a chimney \"<A>\"? Answer \"Yes it does\" or \"No it does not\".", llm=EVAL_LLM) >> SubstringEvaluator("es it does")

if __name__ == "__main__":
    print(run_test(TestDrawTriangle))
```

Now please rewrite the following code with the new format:

INPUT:
```
%s
```
'''

for f in os.listdir("."):
    if '__' in f: continue
    try:
        code = open(f).read()
    except:
        continue

    if 'if __name__ == "__main__":' in code and '>>' in code and 'from evaluator import *' in code and 'from llm' in code:
        pass
    else:
        continue
    if os.path.exists("/tmp/tests/%s" % f):
        continue
    print("RUNNING", f)
    continue

    try:
        def finish(x):
            open("/tmp/tests/%s" % f, "w").write(x)
            return True, ""
        
        Pipeline = prompt%code >> LLMRun() >> PyEvaluator(finish)
        run_test(Pipeline)
    except:
        print("FAIL", f)
        pass
    
    #exit(0)
