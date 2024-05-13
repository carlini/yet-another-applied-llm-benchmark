from evaluator import *

DESCRIPTION = "Test if the model can solve a rather hard dynamic programming problem"

TAGS = ['code', 'c']

question = "A binary 8x8 matrix is 'unholy' if there are no isolated 1s. A 1 is isolated if there isn't another 1 in any of the 4 direct cardinal directions. Write a C program that counts the total number of unholy 8x8 matricies."


step = """To solve this question:
- Use bit arithmetic and an unsigned long to represent the matrix.
- Write a function is_unholy that tests if a matrix is unholy by bit-shifting and masking.

Use a dynamic program to count the number of unholy matricies.
- Recurse on the number of rows the matrix has.
- Enumerate all 2^16 next two rows. This is enough to completely isolate the prior solutions from the next.

Write out a plan for the program, and then implement the plan in C."""

answer = "1121231537486377866"

TestUnholyMatrix = question >> LLMRun() >> ExtractCode(keep_main=True) >> CRun() >> SubstringEvaluator(answer)
TestUnholyMatrixStep = (question + step) >> LLMRun() >> ExtractCode(keep_main=True) >> CRun() >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestUnholyMatrix))



