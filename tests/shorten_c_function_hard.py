from evaluator import *

DESCRIPTION = "Test if the model can significantly shorten a repetitive C functions."

TAGS = ['code', 'c']

question = """
Code golf this function to be a lot shorter. You only get points if it's <300 bytes (not counting whitespace). Keep the function named `count`.

```

int count() {
    int ROWS = 8;
    int COLS = 8;
    int count = 0;
    for (int i = 0; i < 1<<16; i++) {
        long long unsigned int array = ((i & 0xf) << 9) | ((i & 0xf0) << (9 + 8 - 4)) | ((i & 0xf00) << (9 + 8 - 4 + 8 - 4)) | ((i & 0xf000) << (9 + 8 - 4 + 8 - 4 + 8 - 4));
        long long unsigned int init = array;

    long long unsigned int temp = array;

    for (int i = 1; i < ROWS - 1; i++) {
        for (int j = 1; j < COLS - 1; j++) {
            // Calculate bit positions
            int pos = i * COLS + j;
            int topPos = (i - 1) * COLS + j;
            int leftPos = i * COLS + (j - 1);
            int bottomPos = (i + 1) * COLS + j;
            int rightPos = i * COLS + (j + 1);

            // Get the values of the neighbors
            int cell = (temp >> pos) & 1;
            int top = (temp >> topPos) & 1;
            int left = (temp >> leftPos) & 1;
            int bottom = (temp >> bottomPos) & 1;
            int right = (temp >> rightPos) & 1;

            // Sum the values of the neighbors
            int sum = top + left + bottom + right;

            // Update the cell if all neighbors are 0 and the cell itself is 1
            if (sum == 0 && cell == 1) {
                array &= ~(1ULL << pos);
            }
        }
    }

        count += (init == array);
    }
    return count;
}
```
"""

test_case, answer = make_c_test([("count()", "27488")])

def short_enough(num):
    return lambda code: len(code.replace(" ", "").replace("\n", "").replace("\t", "")) < num

step = "\nTo do this follow these steps: \n1. Start out explaining what the function does in words.\n2. Then find a few ways that you can make the function shorter given this explanation.\n3. Write the function as short as possible.\n4. See if you can make it any shorter. Return this as the final answer and call it your final answer. Make sure to name it `count` still."

TestShortenC2Hard = question.replace("<300", "<200") >> LLMRun() >> ExtractCode() >> (PyFunc(short_enough(200)) & (CRun(test_case) >> SubstringEvaluator(answer)))
TestShortenC2 = question >> LLMRun() >> ExtractCode() >> (PyFunc(short_enough(300)) & (CRun(test_case) >> SubstringEvaluator(answer)))
TestShortenC2Step = question + step >> LLMRun() >> ExtractCode() >> (PyFunc(short_enough(300)) & (CRun(test_case) >> SubstringEvaluator(answer)))


if __name__ == "__main__":
    from llm import llm
    print(run_test(TestShortenC2Step))


