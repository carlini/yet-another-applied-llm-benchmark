from evaluator import *

DESCRIPTION = "Test if the model understands the CRC-32 spec well enough to implement it."

TAGS = ['code', 'c']
import zlib

question = 'Write a c program that calculates the crc32 hash of the string "correct horse battery staple" and prints it to stdout. Dont call any builtin crc32 functions.'

answer = "%x"%zlib.crc32(b'correct horse battery staple')

TestCRC32 = question >> LLMRun() >> ExtractCode(keep_main=True) >> Echo() >> CRun() >> SubstringEvaluator(answer, lower=True)


if __name__ == "__main__":
    print(run_test(TestCRC32))

