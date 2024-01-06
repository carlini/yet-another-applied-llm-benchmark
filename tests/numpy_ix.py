from evaluator import *

TAGS = ['explain', 'python']

question = '''I want a function to vectorize

        frame = np.zeros((out_h, out_w, 3), dtype=np.uint8)
        for i, val1 in enumerate(rows):
            for j, val2 in enumerate(cols):
                # Assuming you want to store the pair as tuples in the matrix                                                                                                                                                                                
                frame[i, j] = image[val1, val2]

        out.write(np.array(frame))

what is it called'''

TestPrintHello = question >> LLMRun() >> SubstringEvaluator("ix_")


if __name__ == "__main__":
    print(run_test(TestPrintHello))

