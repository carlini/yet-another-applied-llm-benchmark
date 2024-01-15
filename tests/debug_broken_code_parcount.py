from evaluator import *

DESCRIPTION = "Test if a model can explain a bug in a parallelized wordcount function."

TAGS = ['explain', 'python', 'fix']
import collections

question = """
What is the bug in this code that makes it not count right. (I want to print out 4 arrays un-merged. I'll do the merging later. This is intentional.)

#!/usr/bin/env python3
import json
import multiprocessing

def count_words_in_chunk(start, end, queue):
    '''Count how often each word appears in the given chunk of the file.'''
    word_counts = {}
    with open('/tmp/file.txt', 'r') as f:
        f.seek(start)
        text = f.read(end - start)
        # Avoid cutting words in half at the beginning
        if start != 0:
            text = text.split(' ', 1)[-1]
        # Avoid cutting words in half at the end
        f.seek(end)
        remainder = f.readline()
        text += remainder
        # Tokenize and count words
        for word in text.split():
            word = word.strip().lower()  # Lowercasing for consistent counting
            if word:
                word_counts[word] = word_counts.get(word, 0) + 1
    # Put result to the queue
    queue.put(word_counts)

def main():
    # Get the size of the file
    file_size = 0
    with open('/tmp/file.txt', 'r') as f:
        f.seek(0, 2)
        file_size = f.tell()

    # Calculate chunk sizes for 4 cores
    chunk_size = file_size // 4
    offsets = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    # Last chunk should go until the end of the file
    offsets[-1] = (offsets[-1][0], file_size)

    # Queue for inter-process communication
    queue = multiprocessing.Queue()

    # Start 4 worker processes
    processes = []
    for start, end in offsets:
        p = multiprocessing.Process(target=count_words_in_chunk, args=(start, end, queue))
        processes.append(p)
        p.start()

    # Collect results
    for p in processes:
        p.join()

    # Print results as JSON objects one-per-process
    while not queue.empty():
        word_count = queue.get()
        print(json.dumps(word_count))

if __name__ == "__main__":
    main()


List exactly one reason.
"""

    
TestWhyBuggyPythonCountPar = question >> LLMRun() >> LLMRun("Below is a student's explanation for why some parallel wordcounting code is not working correctly. You don't need to see the full code, just tell me whether or not the student says that the main reason the code is broken is because 'the chunks could contain the same data or be overlapping' or something like this. Saying 'a word might be split in half' is wrong. Saying 'you might miss a word' is also wrong. Here is their answer:\n\n<A>\n\nTell me either 'The student passes' or 'The student fails'.", llm=EVAL_LLM) >> Echo() >> SubstringEvaluator("student passes")


if __name__ == "__main__":
    print(run_test(TestWhyBuggyPythonCountPar))
