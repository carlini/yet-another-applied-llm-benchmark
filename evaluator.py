import subprocess
import pickle
import random
import json
import os
import time
import io
import docker
import inspect

import numpy as np

from PIL import Image

import docker_controller
from docker_controller import invoke_docker, DockerJob


LLM = "eval_llm"
EVAL_LLM = "eval_llm"
VISION_EVAL_LLM = "vision_eval_llm"

def RetryFixCodeErrors(self, conversation, error_message):
    print("OK I HAVE HERE", conversation, error_message)
    return conversation.send_user("I ran the code you suggested but got this wrong output: " + error_message + "\nPlease fix this error and then re-write the entire code block correctly this time.")

class Env:
    docker = None
    container = None
    docker_job = None

class Node:
    def __init__(self, runner):
        self.runner = runner

    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        self.env = env
        self.conv = conv
        self.llm = llm
        self.eval_llm = eval_llm
        self.vision_eval_llm = vision_eval_llm

    def __call__(self, orig_output):
        return self.runner(orig_output)

    def __rshift__(self, other_node):
        if isinstance(other_node, str):
            other_node = StringNode(other_node)
        return ThenNode(self, other_node)
    
    def __rrshift__(self, other_node):
        if isinstance(other_node, str):
            other_node = StringNode(other_node)
        return ThenNode(other_node, self)
    
    def __and__(self, other_node):
        return AndNode(self, other_node)

    def __or__(self, other_node):
        return OrNode(self, other_node)

    def __invert__(self):
        return NotNode(self)

class UntilDone(Node):
    def __init__(self, cond, body, max_iters=100):
        self.cond = cond
        self.body = body
        self.max_iters = max_iters
        
    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        super().setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.cond.setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.body.setup(env, conv, llm, eval_llm, vision_eval_llm)

    def __call__(self, orig_output=None):
        for i in range(self.max_iters):
            print("On iteration", i)
            for output, txt in self.cond(orig_output):
                if output:
                    yield orig_output
                    return
            orig_output = next(self.body(orig_output))
        yield orig_output

    
class ThenNode(Node):
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        super().setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.node1.setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.node2.setup(env=env, conv=conv, llm=llm, eval_llm=eval_llm, vision_eval_llm=vision_eval_llm)

    def __call__(self, orig_output=None):
        for output1 in self.node1(orig_output):
            for output2 in self.node2(output1):
                yield output2

class StringNode(Node):
    def __init__(self, string):
        self.string = string

    def __call__(self, orig_output=""):
        yield self.string
        
class AndNode(ThenNode):
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            for output2, txt2 in self.node2(orig_output):
                yield output1 and output2, (txt1 if not output1 else "") + "\n" + (txt2 if not output2 else "")

class OrNode(ThenNode):
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            for output2, txt2 in self.node2(orig_output):
                yield output1 or output2, txt1 + "\n" + txt2
                
class NotNode(Node):
    def __init__(self, node1):
        self.node1 = node1

    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        super().setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.node1.setup(env, conv, llm, eval_llm, vision_eval_llm)
        
    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            yield not output1, txt1

class PyFunc(Node):
    def __call__(self, x):
        try:
            return [self.runner(x)]
        except:
            return ["Error"]

class Echo(Node):
    def __init__(self):
        pass
    def __call__(self, x):
        print('ECHOING:', x)
        yield x
    
class Setup(Node):
    def __call__(self, x):
        docker_controller.setup_docker(self.env)
        code = inspect.getsource(self.runner)
        to_invoke = self.runner.__name__

        code = code + f"\n\n{to_invoke}()"
        out = invoke_docker(self.env, {"setup.py": code.encode()}, ["python3.11", "setup.py"])
        print('on setup got', out)

        return [out]

class PyEvaluator(Node):
    def __call__(self, x):
        print("I AM RUNNING")
        code = inspect.getsource(self.runner)
        to_invoke = self.runner.__name__

        code = code + f"\n\nprint({to_invoke}())"
        out = invoke_docker(self.env, {"check.py": code.encode()}, ["python3.11", "check.py"])
        print('have here', out)

        return [("True" in out, "")]
    

class SubstringEvaluator(Node):
    def __init__(self, substr, lower=False):
        self.substr = substr
        self.lower = lower

    def __call__(self, output):
        print(output)
        if self.lower:
            cond = self.substr.lower() in output.lower()
        else:
            cond = self.substr in output
            
        if cond:
            yield True, f"Substring {self.substr} found in output. Full log: {output}"
        else:
            yield False, f"Substring {self.substr} not found in output. Full log: {output}"

class EqualEvaluator(Node):
    def __init__(self, goal):
        self.goal = goal

    def __call__(self, output):
        print('cmp', output, self.goal)
        if self.goal == output:
            yield True, f"Goal {self.goal} equal to output. Full log: {output}"
        else:
            yield False, f"Goal {self.goal} not equal to output. Full log: {output}"
            
class ExtractJSON(Node):
    def __init__(self):
        pass

    def try_extract(self, output):
        output = output.replace("```json", "```")
        if "```" in output:
            yield output.split("```")[1]
            out1 = "\n".join(output.split("```")[1::2])
            yield out1
        else:
            yield output
        
    def __call__(self, orig_output):
        if orig_output.count("```") == 2:
            for maybe in self.try_extract(orig_output):
                yield maybe
        else:
            output = self.llm("Take the below answer to my question asking for a JSON output and just return the JSON obcject directly, with no other description, so I can copy it into an editor directly:\n" + orig_output)
            for maybe in self.try_extract(output):
                yield maybe

class ExtractCode(Node):
    def __init__(self, keep_main=False, postfix="", manual=None, lang=None):
        self.keep_main = keep_main
        self.postfix = postfix
        self.manual = manual
        self.lang = lang

    def try_extract(self, output):
        output = output.replace("```python", "```")
        output = output.replace("```html", "```")
        output = output.replace("```c", "```")
        output = output.replace("```cpp", "```")
        output = output.replace("```rust", "```")
        output = output.replace("```sql", "```")
        output = output.replace("```sh", "```")
        output = output.replace("```diff", "```")
        if "```" in output:
            yield output.split("```")[1] + "\n" + self.postfix
            out1 = "\n".join(output.split("```")[1::2])
            #yield out1 + "\n" + self.postfix
        else:
            yield output + "\n" + self.postfix
        
    def __call__(self, orig_output):
        if orig_output.count("```") == 2:
            for maybe in self.try_extract(orig_output):
                yield maybe
            return

        language = ""
        if self.lang is not None:
            language = f"(in {self.lang})"
                
        if self.manual is not None:
            output = self.llm(self.manual.replace("<A>", orig_output))
        elif self.keep_main:
            assert self.postfix == ""
            output = self.llm(f"Take the below answer to my programming question {language} and return just the complete code in a single file so I can copy and paste it into an editor and directly run it. Include any header and main necessary so I can run it by copying this one file. DO NOT MODIFY THE CODE OR WRITE NEW CODE. Here is the code: \n" + orig_output)
        else:
            output = self.llm(f"Take the below answer to my programming question {language} and return just the complete code in a single file so I can copy and paste it into an editor and directly run it. Remove any test cases or example code after the function definition. Remove any main function. I will write those myself. Do include header imports. DO NOT MODIFY THE CODE OR WRITE NEW CODE. Here is the code: \n" + orig_output + ("\nI will be running this code with the following helper functions:\n" + self.postfix if self.postfix else ""))

        print("DO EXTRACT")
        print("HAVE", output)

        for maybe in self.try_extract(output):
            yield maybe



#class LatexCompiler(Node):
#    def __call__(code):
#        open("/tmp/a.tex", "w").write(code)
#        output = os.popen("pdflatex /tmp/a.tex").read()
#        return output

class MakeFile(Node):
    def __init__(self, name):
        self.name = name

    def __call__(self, code):
        yield invoke_docker(self.env, {self.name: code.encode()}, ["echo"])


class PythonRun(Node):
    def __init__(self, test_case="", out_bytes=False):
        self.test_case = test_case
        self.out_bytes = out_bytes

    def __call__(self, code):
        code = code + "\n\n" + self.test_case

        yield invoke_docker(self.env, {"main.py": code.encode()}, ["python3.11", "main.py"], out_bytes=self.out_bytes)

class SQLRun(Node):
    def __init__(self):
        pass

    def __call__(self, code):
        yield invoke_docker(self.env, {"run.sql": code.encode()}, ["sqlite3", "-init", "run.sql", "database.db", ".exit"])
        
class BashRun(Node):
    def __init__(self, test_case="", args=[]):
        self.test_case = test_case
        self.args = args

    def __call__(self, code):
        code = code + "\n\n" + self.test_case

        yield invoke_docker(self.env, {"main.sh": code.encode()}, ["bash", "main.sh", *self.args])

class TerminalRun(Node):
    def __init__(self):
        return

    def __call__(self, code):
        yield invoke_docker(self.env, {}, ["bash", '-c', code])

class RustRun(Node):
    def __init__(self, test_case=""):
        self.test_case = test_case

    def __call__(self, code):
        if 'fn main' in code and 'fn main' in self.test_case:
            code = code.replace('fn main', 'fn __delete_this__main')

        code = code + "\n\n" + self.test_case
            
        yield invoke_docker(self.env, {"main.rs": code.encode(),
                                       "main.sh": "rustc -o a.out main.rs\n./a.out".encode()},
                            ["bash", "main.sh"])

class CRun(Node):
    def __init__(self, test_case="", out_bytes=False):
        self.test_case = test_case
        self.out_bytes = out_bytes

    def __call__(self, code):
        if 'int main' in code and 'int main' in self.test_case:
            code = code.replace('int main', 'int __delete_this__main')

        code = code + "\n\n" + self.test_case
        
        yield invoke_docker(self.env, {"main.c": code.encode(),
                                       "main.sh": "gcc -o a.out main.c -lm\n./a.out".encode()},
                            ["bash", "main.sh"], out_bytes=self.out_bytes)


class StartDockerJob(Node):
    def __init__(self, command, eos_string):
        self.command = command
        self.eos_string = eos_string

    def __call__(self, text):
        self.env.docker_job = DockerJob(self.env.container.id, self.eos_string)
        print("ID", self.env.container.id)
        print("GO!", self.command)
        out = self.env.docker_job(self.command)
        print("DONE")

        yield out

class SendStdoutReceiveStdin(Node):
    def __init__(self):
        pass

    def __call__(self, text):
        yield self.env.docker_job(text)


class CppRun(Node):
    def __init__(self, test_case="", out_bytes=False):
        self.test_case = test_case
        self.out_bytes = out_bytes

    def __call__(self, code):
        if 'int main' in code and 'int main' in self.test_case:
            code = code.replace('int main', 'int __delete_this__main')

        code = code + "\n\n" + self.test_case
        
        yield invoke_docker(self.env, {"main.cpp": code.encode(),
                                       "main.sh": "g++ -o a.out main.cpp -lm\n./a.out".encode()},
                            ["bash", "main.sh"], out_bytes=self.out_bytes)
        
            
class LLMRun(Node):
    def __init__(self, check_prompt="<A>", llm=LLM):
        self.check_prompt = check_prompt
        self.which_llm = llm

    def __call__(self, output):
        print("PASSING", self.check_prompt.replace("<A>", output))
        llm = getattr(self, self.which_llm)
        out = llm(self.check_prompt.replace("<A>", output))
        yield out

class LLMConversation(Node):
    def __init__(self, check_prompt="<A>"):
        self.check_prompt = check_prompt

    def __call__(self, output):
        out = self.conv(self.check_prompt.replace("<A>", output))
        yield out

class SeleniumDraw(Node):
    def __init__(self):
        pass

    def __call__(self, code):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        open("/tmp/a.html", "w").write(code)

        url = 'file:///tmp/a.html'

        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)

        time.sleep(2)

        screenshot_path = '/tmp/a.png'
        browser.save_screenshot(screenshot_path)

        browser.quit()

        time.sleep(1)

        yield Image.open(screenshot_path).convert('RGB')
        

class JSONSubsetEvaluator(Node):
    def __init__(self, goal):
        self.goal = goal
        
    def check(self, goal, output):
        if isinstance(goal, dict) and isinstance(output, dict):
            # Iterate over all key-value pairs in the goal dictionary
            for key, value in goal.items():
                # Check if the key is present in the output
                if key not in output:
                    return False, ""
                # If the value is a dict or list, recursively check
                if isinstance(value, (dict, list)):
                    if not self.check(value, output[key]):
                        return False, ""
                # Otherwise, check if the value matches
                elif output[key] != value:
                    return False, ""
        elif isinstance(goal, list) and isinstance(output, list):
            # Check each element in the goal list
            for item in goal:
                if item not in output:
                    return False, ""
        else:
            # Not a dict or list, so check if the values are equal
            return goal == output, ""
    
        # todo better error message
        return True, ""
        
    def __call__(self, output):
        try:
            output = json.loads(output)
        except:
            yield False, "Failed to parse json"
            return
    
        yield self.check(self.goal, output)

def LLMEvaluator(llm, check_prompt):
    def evaluate(output):
        out = llm.yes_or_no(check_prompt.replace("<A>", output))
        # todo: make the reason better
        yield out, f"LLM says {out}"
    return evaluate

class LLMVisionRun(Node):
    def __init__(self, check_prompt="<A>", llm=VISION_EVAL_LLM):
        self.check_prompt = check_prompt
        self.which_llm = llm

    def __call__(self, output):
        print("RUN VISION")
        llm = getattr(self, self.which_llm)
        try:
            if isinstance(output, bytes):
                img = Image.open(io.BytesIO(output))
            else:
                img = output
            out = llm(self.check_prompt, add_image=img, max_tokens=512)
        except Exception as e:
            out = str(e)
        yield out

class Conversation:
    def __init__(self, llm):
        self.llm = llm
        self.history = []

    def __call__(self, msg):
        self.history.append(msg)
        output = self.llm(self.history)
        self.history.append(output)
        return output

    def __repr__(self):
        return "Conversation(" + repr(self.history) + ")"

def run_test(test):
    from llm import llm, eval_llm, vision_eval_llm
    env = Env()
    test.setup(env, Conversation(llm), llm, eval_llm, vision_eval_llm)

    for success, output in test():
        if success:
            return True
        else:
            pass

    if env.container:
        docker_controller.async_kill_container(env.docker, env.container)

    return False
    

def make_python_test(q_and_a, header=""):
    qs = [header]
    
    for q, a in q_and_a:
        qs.append(f"""
answer = {q}
expected = {a}
assert answer == expected, f'Wrong answer; got {{answer}} instead of {{expected}}'""")
    qs.append("print('All tests passed')")

    return "\n".join(qs), "All tests passed"
    

def make_c_test(q_and_a, header=""):
    qs = []

    qs.append("#include<stdio.h>\n#include<stdlib.h>\nint main() {")
    qs.append(header)
    for q, a in q_and_a:
        qs.append(f"""
int answer = {q};
int expected = {a};
if (answer != expected) {{
    printf("Wrong answer; got %d instead of %d.\\n", answer, expected);
    exit(1);
}}""")
    qs.append('printf("All tests passed\\n");')

    qs.append("}");
    
    return "\n".join(qs), "All tests passed"
        
    

