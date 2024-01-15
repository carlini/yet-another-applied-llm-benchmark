from evaluator import *

DESCRIPTION = "Test if a model can identify the _ix function as a method for simplifying some code."

TAGS = ['explain', 'python']

question = '''I want to vectorize a function

        frame = np.zeros((out_h, out_w, 3), dtype=np.uint8)
        for i, val1 in enumerate(rows):
            for j, val2 in enumerate(cols):
                for j, val3 in enumerate(ch):
                    # Assuming you want to store the pair as tuples in the matrix
                    frame[i, j, k] = image[val1, val2, val3]

        out.write(np.array(frame))

with a simple numpy function that does something like this what is it called'''

TestNumpyIx = question >> LLMRun() >> SubstringEvaluator("ix_")


if __name__ == "__main__":
    print(run_test(TestNumpyIx))

