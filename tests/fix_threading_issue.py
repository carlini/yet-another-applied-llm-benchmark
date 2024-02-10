from evaluator import *


DESCRIPTION = "Test if the model can explain a poorly worded error message in a short threaded python program."

TAGS = ['code', 'python', 'explain']


question = """In this program

from multiprocessing import Pool
from openai import OpenAI

txt = open("/tmp/aa.txt").read().split("\n\n")

from multiprocessing import Pool
import subprocess

client = OpenAI(api_key="sk-XXXXXXXXXXXXXX")
def create_speech_file(index, text):
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
	input=text
    )
    filename = f"output{index}.mp3"
    response.stream_to_file(filename)
    return filename

def merge_mp3(files, output):
    with open("filelist.txt", "w") as file:
	for f in files:
            file.write(f"file '{f}'\n")

    cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "filelist.txt", "-c", "copy", output]
    subprocess.run(cmd)

if __name__ == '__main__':
    # Step 1: Parallelize speech file creation                                                                                                                            
    with Pool(8) as pool:
	mp3_files = pool.starmap(create_speech_file, enumerate(txt))

    # Step 2: Merge the generated MP3 files                                                                                                                               
    output_file = "merged_output.mp3"
    merge_mp3(mp3_files, output_file)

Why am I getting this error?

Exception in thread Thread-3:
Traceback (most recent call last):
  File "/opt/homebrew/Cellar/python@3.9/3.9.16/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 980, in _bootstrap_inner
    self.run()
  File "/opt/homebrew/Cellar/python@3.9/3.9.16/Frameworks/Python.framework/Versions/3.9/lib/python3.9/threading.py", line 917, in run
    self._target(*self._args, **self._kwargs)
  File "/opt/homebrew/Cellar/python@3.9/3.9.16/Frameworks/Python.framework/Versions/3.9/lib/python3.9/multiprocessing/pool.py", line 576, in _handle_results
    task = get()
  File "/opt/homebrew/Cellar/python@3.9/3.9.16/Frameworks/Python.framework/Versions/3.9/lib/python3.9/multiprocessing/connection.py", line 251, in recv
    return _ForkingPickler.loads(buf.getbuffer())
TypeError: __init__() missing 2 required keyword-only arguments: 'response' and 'body'

"""

TestQuestionThreadedFix = question >> LLMRun() >> LLMRun("I showed a student some code with a bug. I then tested their understanding by asking them to explain hwo to fix the bug. I'm going to show you their answer, I want you to evaluate whether or not their answer says something to the effect of \"The function create_speech_file is raising an exception that can not be pickled.\". Do not judge their reasonining, or if they know how to fix it, just tell me if they correctly identified that there is a crash in the create_speech_file function. \n Student Answer: \"<A>\"\n\n Think out loud then answer either \"The student passes\" or \"The student fails\".", llm=EVAL_LLM) >> SubstringEvaluator("student passes")


if __name__ == "__main__":
    print(run_test(TestQuestionThreadedFix))
