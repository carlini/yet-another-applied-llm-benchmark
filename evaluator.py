## Copyright (C) 2024, Nicholas Carlini <nicholas@carlini.com>.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import pickle
import random
import json
import os
import time
import io
import docker
import inspect
import re

import numpy as np

from PIL import Image

import docker_controller
from docker_controller import invoke_docker, DockerJob


## Constants that define which model we're supposed to be using:
LLM = "llm"                         # The LLM under evaluation
EVAL_LLM = "eval_llm"               # A good LLM that can act as a judge
VISION_EVAL_LLM = "vision_eval_llm" # And a good judge for vision tasks
PYTHON_ENV = "python3.11"            # The version of python to use

class Env:
    """
    An environment that holds the local variables for each test case.
    """

    # The docker object we're running the test in
    docker = None

    # (Optionally, if in unsafe mode, the fake docker object)
    fake_docker_id = None

    # The docker container we're running the tests in
    container = None

    # A DockerJob object, if the test case requires it.
    # These objects allow the test to interact with stdin/out
    # of a process running in the docker container and must be
    # persistant across multiple classes in the test case.
    docker_job = None
    
class Reason:
    """
    A class to keep track of the solution path of a test.
    """
    def __init__(self, node, children):
        self.node = node
        self.children = children

    def __repr__(self):
        return repr((self.node, self.children))
        
    
class Node:
    """
    A node forms the operations in the computation graph for evaluating a test case;
    the most important object in this file. A test case might look like

        Node1 >> Node2 >> (Node3 & Node4)

    Each of these operators that connects nodes return a new node. So this graph
    would be equivalent to writing:

        ThenNode(ThenNode(Node1, Node2), AndNode(Node3, Node4))

    Once the computation graph has been constructed, evaluation is performed by
    calling __call__ on the root node, that then passes off the evalaution process
    as defined by each of the node types.
    """

    def __init__(self, runner):
        """
        Many sub-classes take a single argument, the runner, which is a function
        that should be executed for performing this node's computation.
        """
        self.runner = runner
    
    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        """
        Once the graph has been constructed, before running __call__ to evaluate
        the test case, we run setup() on each of the nodes to pass all the
        necessary context. 
        """
        self.env = env
        self.conv = conv
        self.llm = llm
        self.eval_llm = eval_llm
        self.vision_eval_llm = vision_eval_llm

    def __call__(self, orig_output=""):
        """
        Evaluate the test case, starting at this node. This is the main entry
        point for the evaluation process.

        Returns two arguments:
        1. The output of the current node that should be passed to the next node.
        2. A Reason object that explains how the output was generated for debugging.
        
        """
        raise NotImplementedError()
        
    def __rshift__(self, other_node):
        """
        Add the >> operator, which creates a ThenNode.
        Wrap any strings in a StringNode first, to allow for code like

            SetupNode >> "command to run" >> LLMRunNode
        """
        
        if isinstance(other_node, str):
            other_node = StringNode(other_node)
        return ThenNode(self, other_node)
    
    def __rrshift__(self, other_node):
        """
        If a string is the first node, we need to special case the
        rrshift operator, since we can't override the string class.
        Allows the (very common) pattern of

            "command to run" >> LLMRunNode
        """
        if isinstance(other_node, str):
            other_node = StringNode(other_node)
        return ThenNode(other_node, self)
    
    def __and__(self, other_node):
        return AndNode(self, other_node)

    def __or__(self, other_node):
        return OrNode(self, other_node)

    def __invert__(self):
        return NotNode(self)

class StringNode(Node):
    def __init__(self, string):
        """
        A boring node, just returns the string.
        """
        self.string = string

    def __call__(self, orig_output=""):
        """
        Just pass whatever the provided constant string is to the next node.
        """
        yield self.string, Reason(type(self), self.string)
        

class ThenNode(Node):
    """
    Perform two operations in sequence. The output of node1 is passed to node2.
    """
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        super().setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.node1.setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.node2.setup(env=env, conv=conv, llm=llm, eval_llm=eval_llm, vision_eval_llm=vision_eval_llm)

    def __call__(self, orig_output=None):
        for output1, response1 in self.node1(orig_output):
            for output2, response2 in self.node2(output1):
                yield output2, Reason(type(self), (response1, response2))

class AndNode(ThenNode):
    """
    An evaluation node that returns true if both outputs are true.
    """
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            for output2, txt2 in self.node2(orig_output):
                yield output1 and output2, Reason(type(self), (txt1, txt2, output1 and output2))

class OrNode(ThenNode):
    """
    An evaluation node that returns true if either outputs are true.
    """
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            for output2, txt2 in self.node2(orig_output):
                yield output1 or output2, Reason(type(self), (txt1, txt2, output1 or output2))
                
class NotNode(Node):
    """
    An evaluation node that negates the prior answer.
    """
    def __init__(self, node1):
        self.node1 = node1

    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        super().setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.node1.setup(env, conv, llm, eval_llm, vision_eval_llm)
        
    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            yield not output1, Reason(type(self), [txt1, not output1])

class PyFunc(Node):
    """
    A node that just runs a python function on the prior result.
    If the code crashes then just return an error.
    """
    def __call__(self, x):
        try:
            out = self.runner(x)
            if type(out) == tuple:
                ok, log = out
                return [(ok, Reason(type(self), (log, ok)))]
            else:
                return [(out, Reason(type(self), ("", out)))]
        except:
            return [("", Reason(type(self), ["Error", False]))]

class Echo(Node):
    """
    A no-op node that helps debug test cases by printing whatever's being
    passed along the pipe. Kind of like the Unix tee command.
    """
    def __init__(self):
        pass

    def __call__(self, x):
        print('ECHOING:', x)
        yield x, Reason(type(self), None)
    
class Setup(Node):
    """
    A node that starts up a new Docker environment with a specific setup file.

    Even though the argument is a method, this function needs to be able to
    extract the string representation of that function so it can be executed
    in the context of the docker environment.
    """
    def __call__(self, x):
        docker_controller.setup_docker(self.env)
        code = inspect.getsource(self.runner)
        to_invoke = self.runner.__name__

        code = code + f"\n\n{to_invoke}()"
        out = invoke_docker(self.env, {"setup.py": code.encode()}, [PYTHON_ENV, "setup.py"])

        return [(out, Reason(type(self), None))]

class PyEvaluator(Node):
    """
    A node that runs a python program within the docker environment to judge whether
    or not the test case is solved.

    Even though the argument is a method, this function needs to be able to
    extract the string representation of that function so it can be executed
    in the context of the docker environment.
    """
    def __call__(self, x):
        code = inspect.getsource(self.runner)
        to_invoke = self.runner.__name__

        code = code + f"\n\nprint('final: ' + str({to_invoke}()))"
        out = invoke_docker(self.env, {"check.py": code.encode()}, [PYTHON_ENV, "check.py"])

        return [("final: True" in out, Reason(type(self), [out, "final: True" in out]))]
    

class SubstringEvaluator(Node):
    """
    An evaluation node that checks if a substring is in the output.
    """
    def __init__(self, substr, lower=False):
        self.substr = substr
        self.lower = lower

    def __call__(self, output):
        if self.lower:
            cond = self.substr.lower() in output.lower()
        else:
            cond = self.substr in output
            
        if cond:
            yield True, Reason(type(self), [self.substr, True])
        else:
            yield False, Reason(type(self), [self.substr, False])

class ContainsIntEvaluator(Node):
    """
    An evaluation node that checks if a given integer is in the output.
    """
    def __init__(self, num):
        self.num = num

    def __call__(self, output):
        all_integers = re.findall(r'-?[\d,]*\d+\.?\d*', output)
        all_integers = [x.replace(",", "") for x in all_integers]
        if str(self.num) in all_integers:
            yield True, Reason(type(self), [self.num, True])
        else:
            yield False, Reason(type(self), [self.num, False])
            
class EqualEvaluator(Node):
    """
    An evaluation node that checks if the output is equal to a given string.
    """
    def __init__(self, goal):
        self.goal = goal

    def __call__(self, output):
        if self.goal == output:
            yield True, Reason(type(self), [self.goal, True])
        else:
            yield False, Reason(type(self), [self.goal, False])

class UntilDone(Node):
    """
    A node that will loop a specific body node until the condition returns true and it's finished.

    This node is useful when you want a model to, e.g., iterative interact
    with a sqlite database until it's completed some task.
    """
    def __init__(self, cond, body, max_iters=100):
        self.cond = cond
        self.body = body
        self.max_iters = max_iters
        
    def setup(self, env, conv, llm, eval_llm, vision_eval_llm):
        super().setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.cond.setup(env, conv, llm, eval_llm, vision_eval_llm)
        self.body.setup(env, conv, llm, eval_llm, vision_eval_llm)

    def __call__(self, orig_output=None):
        log = []
        for i in range(self.max_iters):
            for output, txt in self.cond(orig_output):
                if output:
                    yield orig_output, Reason(type(self), log)
                    return
            orig_output, partial = next(self.body(orig_output))
            log.append(partial)
        yield orig_output, Reason(type(self), log)
            
class ExtractJSON(Node):
    """
    A node that extracts a JSON object from the response.

    Usually you can just extract the json blob out of the response,
    but if the response contains multiple possible JSON blobs,
    then this node queries the model again asking it for just the JSON.
    """
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
                yield maybe, Reason(type(self), [maybe])
        else:
            output = self.llm("Take the below answer to my question asking for a JSON output and just return the JSON obcject directly, with no other description, so I can copy it into an editor directly:\n" + orig_output)
            for maybe in self.try_extract(output):
                yield maybe, Reason(type(self), [maybe])

class ExtractCode(Node):
    """
    A node that extracts code from the response

    Usually you can just extract the code out of the response,
    but if the response contains multiple possible code objects,
    then this node queries the model again asking it for just the code.
    """
    def __init__(self, keep_main=False, postfix="", manual=None, lang=None):
        self.keep_main = keep_main
        self.postfix = postfix
        self.manual = manual
        self.lang = lang

    def try_extract(self, output):
        output = re.sub('```[a-z]*', '```', output)
        if "```" in output:
            ans = output.split("```")[1] + "\n" + self.postfix
        else:
            ans = output + "\n" + self.postfix
        yield ans
        
    def __call__(self, orig_output):
        if orig_output.count("```") == 2:
            for maybe in self.try_extract(orig_output):
                yield maybe, Reason(type(self), maybe)
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

        for maybe in self.try_extract(output):
            yield maybe, Reason(type(self), maybe)

class MakeFile(Node):
    """
    A node that makes a new file within the docker environment.
    """
    def __init__(self, name):
        self.name = name

    def __call__(self, code):
        out = invoke_docker(self.env, {self.name: code.encode()}, ["echo"])
        yield out, Reason(type(self), (code, out))


class PythonRun(Node):
    """
    A node that runs the output from the prior command as a python function.

    Optionally append a set of test cases to the code that's been provided.
    """
    def __init__(self, test_case="", out_bytes=False):
        self.test_case = test_case
        self.out_bytes = out_bytes

    def __call__(self, code):
        code = code + "\n\n" + self.test_case

        out = invoke_docker(self.env, {"main.py": code.encode()}, [PYTHON_ENV, "main.py"], out_bytes=self.out_bytes)
        yield out, Reason(type(self), (code, out))

class SQLRun(Node):
    """
    A node that runs the output from the prior command as a sqlite function.
    """
    def __init__(self):
        pass

    def __call__(self, code):
        out = invoke_docker(self.env, {"run.sql": code.encode()}, ["sqlite3", "-init", "run.sql", "database.db", ".exit"])
        yield out, Reason(type(self), (code, out))
        
class BashRun(Node):
    """
    A node that runs the output from the prior command as a bash script.
    """
    def __init__(self, test_case="", args=[]):
        self.test_case = test_case
        self.args = args

    def __call__(self, code):
        code = code + "\n\n" + self.test_case

        out = invoke_docker(self.env, {"main.sh": code.encode()}, ["bash", "main.sh", *self.args])
        yield out, Reason(type(self), (code, out))

class TerminalRun(Node):
    """
    A node that directly runs a command line argument in the terminal.
    """
    def __init__(self):
        return

    def __call__(self, code):
        if code:
            out = invoke_docker(self.env, {"main.sh": code.encode()}, ["bash", "main.sh"])
        else:
            out = ""
        yield out, Reason(type(self), (code, out))

class RustRun(Node):
    """
    A node that runs the output from the prior command as a python function.

    Optionally append a set of test cases to the code that's been provided.
    """
    def __init__(self, test_case=""):
        self.test_case = test_case

    def __call__(self, code):
        if 'fn main' in code and 'fn main' in self.test_case:
            code = code.replace('fn main', 'fn __delete_this__main')

        code = code + "\n\n" + self.test_case
            
        out = invoke_docker(self.env, {"main.rs": code.encode(),
                                       "main.sh": "rustc -o a.out main.rs\n./a.out".encode()},
                            ["bash", "main.sh"])
        yield out, Reason(type(self), (code, out))

class CRun(Node):
    """
    A node that runs the output from the prior command as a c function.

    Optionally append a set of test cases to the code that's been provided.
    """
    def __init__(self, test_case="", out_bytes=False, gccflags="", argv=""):
        self.test_case = test_case
        self.out_bytes = out_bytes
        self.gccflags = gccflags
        self.argv = argv

    def __call__(self, code):
        if 'int main' in code and 'int main' in self.test_case:
            code = code.replace('int main', 'int __delete_this__main')

        code = code + "\n\n" + self.test_case
        
        out = invoke_docker(self.env, {"main.c": code.encode(),
                                       "main.sh": f"gcc -o a.out main.c -lm {self.gccflags}\n./a.out {self.argv}".encode()},
                            ["bash", "main.sh"], out_bytes=self.out_bytes)
        yield out, Reason(type(self), (code, out))


class CppRun(Node):
    """
    A node that runs the output from the prior command as a c++ function.

    Optionally append a set of test cases to the code that's been provided.
    """
    def __init__(self, test_case="", out_bytes=False):
        self.test_case = test_case
        self.out_bytes = out_bytes

    def __call__(self, code):
        if 'int main' in code and 'int main' in self.test_case:
            code = code.replace('int main', 'int __delete_this__main')

        code = code + "\n\n" + self.test_case
        
        out = invoke_docker(self.env, {"main.cpp": code.encode(),
                                       "main.sh": "g++ -o a.out main.cpp -lm\n./a.out".encode()},
                            ["bash", "main.sh"], out_bytes=self.out_bytes)
        yield out, Reason(type(self), (code, out))
        

class StartDockerJob(Node):
    """
    Start a new process within the docker container that's termainl interactive.

    This lets us test models that expect to be able to interface with other pieces
    of software by connecting the llm to stdin and stdout, sending data to the
    program and then reading the output back.
    """
    def __init__(self, command, eos_string):
        self.command = command
        self.eos_string = eos_string

    def __call__(self, text):
        self.env.docker_job = DockerJob(self.env.container.id if 'id' in dir(self.env.container) else self.env.container, self.eos_string)
        out = self.env.docker_job(self.command)

        yield out, Reason(type(self), (text, out))

class SendStdoutReceiveStdin(Node):
    """
    This node takes a given piece of text and sends it to the stdin of whatever
    the current running DockerJob is. It then waits for the running process to handle
    this input, and returns the output that the DockerJob returned from stdout.
    """
    def __init__(self):
        pass

    def __call__(self, text):
        out = self.env.docker_job(text)
        yield out, Reason(type(self), (out,))

            
class LLMRun(Node):
    """
    A node to invoke a language model on any given text.

    This is the core function that allows us to evaluate the capabilities of any model.
    """
    def __init__(self, check_prompt="<A>", llm=LLM):
        self.check_prompt = check_prompt
        self.which_llm = llm

    def __call__(self, output):
        llm = getattr(self, self.which_llm)
        to_send = self.check_prompt.replace("<A>", output)
        out = llm(to_send)
        yield out, Reason(type(self), (to_send, out))

class LLMConversation(Node):
    """
    A node to invoke a language model on any given text, but keeps state.

    This node allows us to send messages that refer to prior messages, whereas
    LLMRun is just a stateless operation.
    """
    def __init__(self, check_prompt="<A>"):
        self.check_prompt = check_prompt

    def __call__(self, output):
        to_send = self.check_prompt.replace("<A>", output)
        out = self.conv(to_send)
        yield out, Reason(type(self), (to_send, out))

class SeleniumDraw(Node):
    """
    A node that creates a new HTML page, renders it in chrome, and then
    captures the output with Selenium.
    """
    def __init__(self):
        pass

    def __call__(self, code):
        #try:
        if 1:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            chrome_options = Options()
            #chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
    
            r = random.randint(0, 1000000)
            
            open("/tmp/a%r.html"%r, "w").write(code)
    
            url = 'file:///tmp/a%d.html'%r
    
            browser = webdriver.Chrome(options=chrome_options)
            browser.get(url)
    
            time.sleep(2)
    
            screenshot_path = '/tmp/a%d.png'%r
            browser.save_screenshot(screenshot_path)
    
            browser.quit()
    
            time.sleep(1)
    
            img = Image.open(screenshot_path).convert('RGB')
    
            # get png data
            img_data = io.BytesIO()
            img.save(img_data, format="PNG")
            img_data.seek(0)
            img_data = img_data.read()
            
            
            yield img_data, Reason(type(self), img_data)

        try:
            pass
    
        except:
            yield b"", Reason(type(self), b"")
        

class JSONSubsetEvaluator(Node):
    def __init__(self, goal):
        self.goal = goal
        
    def check(self, goal, output):
        if isinstance(goal, dict) and isinstance(output, dict):
            # Iterate over all key-value pairs in the goal dictionary
            for key, value in goal.items():
                # Check if the key is present in the output
                if key not in output:
                    return False
                # If the value is a dict or list, recursively check
                if isinstance(value, (dict, list)):
                    if not self.check(value, output[key]):
                        return False
                # Otherwise, check if the value matches
                elif output[key] != value:
                    return False
        elif isinstance(goal, list) and isinstance(output, list):
            # Check each element in the goal list
            for item in goal:
                if item not in output:
                    return False, Reason(self, ["Item not present", item])
        else:
            # Not a dict or list, so check if the values are equal
            if goal == output:
                return True
            else:
                return False
    
        # todo better error message
        return True
        
    def __call__(self, output):
        try:
            output = json.loads(output)
        except:
            yield False, Reason(type(self), [self.goal, False])
            return

        ok = self.check(self.goal, output)
        yield ok, Reason(type(self), [self.goal, ok])

class LLMVisionRun(Node):
    """
    A node to evalaute an image output from a prior operation. Invokes the
    vision evaluation model.
    """
    def __init__(self, check_prompt="<A>", llm=VISION_EVAL_LLM):
        self.check_prompt = check_prompt
        self.which_llm = llm

    def __call__(self, output):
        llm = getattr(self, self.which_llm)
        try:
            if isinstance(output, bytes):
                img = Image.open(io.BytesIO(output))
            else:
                img = output
            out = llm(self.check_prompt, add_image=img, max_tokens=512)
        except Exception as e:
            out = str(e)
        yield out, Reason(type(self), (self.check_prompt, out))

class Conversation:
    """
    An object that keeps track of the conversation history between the
    model and the test case prior questions/steps.
    """
    def __init__(self, llm,preample = ''):
        self.llm = llm
        self.history = []
        self.preample = preample

    def __call__(self, msg):
        if len(self.history)==0:
            msg = self.preample + msg        
        self.history.append(msg)
        output = self.llm(self.history)
        self.history.append(output)
        return output

    def __repr__(self):
        return "Conversation(" + repr(self.history) + ")"

def run_test(test):
    """
    A helper function to run just one specific test case.
    Used to debug tests by running each file directly.
    """
    from llm import llm, eval_llm, vision_eval_llm
    env = Env()
    test.setup(env, Conversation(llm), llm, eval_llm, vision_eval_llm)

    ok = False
    for success, output in test():
        if success:
            ok = True
            break

    import create_results_html
    fmt = create_results_html.format_markdown(output)
    while '\n\n' in fmt:
        fmt = fmt.replace('\n\n', '\n')
    fmt = fmt.replace("\n#", "\n\n#")
    print(fmt)
        
    if env.container:
        docker_controller.async_kill_container(env.docker, env.container)

    return ok
    

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
        
    

