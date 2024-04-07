from evaluator import *

DESCRIPTION = "Test if the model can significantly shorten a repetitive C functions."

TAGS = ['code', 'c']

question = """
Code golf this function to be a lot shorter. You only get points if it's <300 bytes (not counting whitespace). Keep the name `stepper`.

```
void stepper(int xw) {
  int Steps = 0;
  for (int x = 0; x < xw; x++) {
    switch (Steps) {
      case 0:
        digitalWrite(1, 0);
        digitalWrite(2, 0);
        digitalWrite(3, 0);
        digitalWrite(4, 1);
        break;
      case 1:
        digitalWrite(1, 0);
        digitalWrite(2, 0);
        digitalWrite(3, 1);
        digitalWrite(4, 1);
        break;
      case 2:
        digitalWrite(1, 0);
        digitalWrite(2, 0);
        digitalWrite(3, 1);
        digitalWrite(4, 0);
        break;
      case 3:
        digitalWrite(1, 0);
        digitalWrite(2, 1);
        digitalWrite(3, 1);
        digitalWrite(4, 0);
        break;
      case 4:
        digitalWrite(1, 0);
        digitalWrite(2, 1);
        digitalWrite(3, 0);
        digitalWrite(4, 0);
        break;
      case 5:
        digitalWrite(1, 1);
        digitalWrite(2, 1);
        digitalWrite(3, 0);
        digitalWrite(4, 0);
        break;
      case 6:
        digitalWrite(1, 1);
        digitalWrite(2, 0);
        digitalWrite(3, 0);
        digitalWrite(4, 0);
        break;
      case 7:
        digitalWrite(1, 1);
        digitalWrite(2, 0);
        digitalWrite(3, 0);
        digitalWrite(4, 1);
        break;
      default:
        digitalWrite(1, 0);
        digitalWrite(2, 0);
        digitalWrite(3, 0);
        digitalWrite(4, 0);
        break;
    }
    Steps = (Steps + 1) % 8;
  }
}
```
"""

test_case, answer = make_c_test([("(stepper(100),out)", "-1475775710")], extra_methods="""
#include <stdio.h>

int out = 0;
int digitalWrite(int pin, int value) {
  out *= 101;
  out += pin;
  out *= 97;
  out += value;
  return out;
}
""")

def short_enough(num):
    return lambda code: len(code.replace(" ", "").replace("\n", "").replace("\t", "")) < num

step = "\nTo do this follow these steps: \n1. start out by creating a table of the values that are being written to the pins.\n2. Then find an expression for this.\n3. Write the function as short as possible.\n4. See if you can make it any shorter. Return this as the final answer and call it your final answer. Make sure to name it stepper still."

TestShortenCHard = question.replace("<300", "<200") >> LLMRun() >> ExtractCode() >> (PyFunc(short_enough(200)) & (CRun(test_case) >> SubstringEvaluator(answer)))
TestShortenC = question >> LLMRun() >> ExtractCode() >> (PyFunc(short_enough(300)) & (CRun(test_case) >> SubstringEvaluator(answer)))
TestShortenCStep = question + step >> LLMRun() >> ExtractCode() >> (PyFunc(short_enough(300)) & (CRun(test_case) >> SubstringEvaluator(answer)))


if __name__ == "__main__":
    from llm import llm
    print(run_test(TestShortenCHard))

