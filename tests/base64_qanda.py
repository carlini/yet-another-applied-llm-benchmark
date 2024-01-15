from evaluator import *

DESCRIPTION = "Test if a model will follow instructions to the letter without lots of cajoling. Thinking in base64 is also interesting."

TAGS = ['explain', 'fun']
import base64 

question = """
Read this base64 string, think about the answer, and type just the answer in base64. You're entire answer must be base64.

V2hhdCBpcyBvbmUgeWVhciBhZnRlciB3aGVuIFByZXNpZGVudCBnZW9yZ2Ugd2FzaGluZ3RvbiBib3JuPw==
"""

TestBase64Thought = question >> LLMRun() >> PyFunc(lambda x: base64.b64decode(x).decode('utf-8')) >> SubstringEvaluator("1733")

if __name__ == "__main__":
    print(run_test(TestBase64Thought))

