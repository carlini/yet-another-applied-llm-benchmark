from evaluator import *

DESCRIPTION = "Test if the model can generate a program that prints \"hello world\" when run either as a C or a python program."

TAGS = ['code', 'python']

question = 'Write a single file that I can save as foo.c.py that I can run as either a C program or a python program, and so both will print "hello world". Specifically if I run `python foo.c.py` or `gcc foo.c.py && ./a.out` I should see "hello world" printed to the console.'

answer = "hello world"

TestPrintHelloPoly = question >> LLMRun() >> ExtractCode(keep_main=True) >> ((PythonRun() >> SubstringEvaluator(answer)) & (CRun() >> SubstringEvaluator(answer)))

question2 = '''
Write a single file that I can save as foo.py.rs that I can run as either a rust program or a python program, and so both will print "hello world". Specifically if I run `python foo.py.rs` or `rustc -o a.out foo.py.rs && ./a.out` I should see "hello world" printed to the console.

To help you out, here's a valid answer for how to do this in C:

```
#include <stdio.h>
#define sdf b /*                                                                                                                 
print("hello world")                                                                                                             
"""                                                                                                                              
#define wer b */

int main() {
  printf("hello world\n");
}

#define ert s """
```
'''

TestPrintHelloPoly = question >> LLMRun() >> ExtractCode(keep_main=True) >> ((PythonRun() >> SubstringEvaluator(answer)) & (CRun() >> SubstringEvaluator(answer)))
TestPrintHelloPoly2 = question2 >> LLMRun() >> ExtractCode(keep_main=True) >> ((PythonRun() >> SubstringEvaluator(answer)) & (RustRun() >> SubstringEvaluator(answer)))


if __name__ == "__main__":
    print(run_test(TestPrintHelloPoly2))


