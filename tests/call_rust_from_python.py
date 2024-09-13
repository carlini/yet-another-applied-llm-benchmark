from evaluator import *

DESCRIPTION = "Test if the model can write rust code that can be imported from python and knows how to build it."

TAGS = ['rust', 'c', 'python', 'code']

question = """I want to call some rust code from python on a linux machine. Specifically, I want to be able to run

python3 -c 'import magic; print(magic.do_add(3, 4))'

and have it give me the sum of these numbers. Here, do_add should be a rust function that adds two integers.

Please give me a complete set of instructions for how to make this run, so that when I run this code as-is it will work.
"""

question2 = """
Now please conver this answer into a JSON array that packages it all up so I don't need to think and can just copy files to specific locations and then run things. Format your answer

{"path/to/file": "contents of rust file",
 "path/to/python_file": "contents of any necessary python file that exposes do_add",
 "build.sh": "contents of a bash file to build the project",
 ...  # any other files necessary
}


The only thing I will do is put files in the right place and run `bash build.sh`. Do not give any explanation of the code. ONLY ANSWER WITH A SINGLE JSON OBJECT. Your answer should start ```json and end with ```.
"""

def is_ok():
    import os
    os.popen("bash build.sh").read()
    
    return os.popen("python3 -c 'import magic; print(magic.do_add(31, 11))'").read() == "42\n"

    
TestCallRustFromPy = question >> LLMConversation() >> LLMConversation(question2) >> ExtractJSON() >> MakeFilesFromJSON() >> PyEvaluator(is_ok)
TestCallCFromPy = question.replace("rust", "C") >> LLMConversation() >> LLMConversation(question2.replace("rust", "C")) >> ExtractJSON() >> MakeFilesFromJSON() >> PyEvaluator(is_ok)


if __name__ == "__main__":
    print(run_test(TestCallRustFromPy))


