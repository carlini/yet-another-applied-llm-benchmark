import subprocess
from PIL import Image
import random
import json
import numpy as np
import os

def python_evaluator(criteria, answer):

    score = []
    
    for test_case, condition in criteria.test_cases:
        open("/tmp/a.py", "w").write(code+"\n\n"+test_case)
        output = os.popen("python3 /tmp/a.py").read()
        
        score.append(condition(output))

    return np.mean(score)


def llm_evaluator(criteria, answer):
    pass


def substring_evaluator(criteria, answer):
    if criteria.substr:
        return criteria.substr in answer
    elif criteria.substrs:
        if criteria.mode == 'all':
            return all(x in answer for x in criteria.substrs)
        elif criteria.mode == 'any':
            return any(x in answer for x in criteria.substrs)
        else:
            raise
    else:
        raise
            

def RetryFixCodeErrors(conversation, error_message):
    print("OK I HAVE HERE", conversation, error_message)
    return conversation.send_user("I ran the code you suggested but got this wrong output: " + error_message + "\nPlease fix this error and then re-write the entire code block correctly this time.")


def PythonRun(test_case):
    def run(code):
        with open("/tmp/a.py", "w") as file:
            file.write(code + "\n\n" + test_case)

        # Running the Python script and capturing stdout and stderr
        process = subprocess.Popen(["python3", "/tmp/a.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decoding from bytes to string and returning both
        yield stdout.decode() + stderr.decode()

    return run

def BashRun():
    def run(code):
        with open("/tmp/a.sh", "w") as file:
            file.write(code)

        print(code)
        # Running the Python script and capturing stdout and stderr
        #process = subprocess.Popen(["bash", "/tmp/a.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #stdout, stderr = process.communicate()

        # Decoding from bytes to string and returning both
        yield stdout.decode() + stderr.decode()

    return run

def CRun(test_case):
    def run(code):
        print("DO C RUN")
        if 'int main' in code and 'int main' in test_case:
            code = code.replace('int main', 'int __delete_this__main')
        
        with open("/tmp/a.c", "w") as file:
            file.write(code + "\n\n" + test_case)

        randn = random.randint(0, 1000000)
            
        # Running the Python script and capturing stdout and stderr
        process = subprocess.Popen(["gcc", "-o", "/tmp/a%d.out"%randn, "/tmp/a.c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout0, stderr0 = process.communicate()

        if os.path.exists("/tmp/a%d.out"%randn):
            process = subprocess.Popen(["/tmp/a%d.out"%randn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout1, stderr1 = process.communicate()
        else:
            stdout1, stderr1 = b"", b""

        print([stdout0.decode() + stderr0.decode() + stdout1.decode() + stderr1.decode()])
        # Decoding from bytes to string and returning both
        return [stdout0.decode() + stderr0.decode() + stdout1.decode() + stderr1.decode()]

    return run

def RustRun(test_case):
    def run(code):
        print("DO C RUN")
        if 'fn main' in code and 'fn main' in test_case:
            code = code.replace('fn main', 'fn __delete_this__main')
        
        with open("/tmp/a.rs", "w") as file:
            file.write(code + "\n\n" + test_case)

        randn = random.randint(0, 1000000)
            
        # Running the Python script and capturing stdout and stderr
        process = subprocess.Popen(["rustc", "-o", "/tmp/a%d.out"%randn, "/tmp/a.rs"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout0, stderr0 = process.communicate()

        if os.path.exists("/tmp/a%d.out"%randn):
            process = subprocess.Popen(["/tmp/a%d.out"%randn], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout1, stderr1 = process.communicate()
        else:
            stdout1, stderr1 = b"", b""

        print([stdout0.decode() + stderr0.decode() + stdout1.decode() + stderr1.decode()])
        # Decoding from bytes to string and returning both
        return [stdout0.decode() + stderr0.decode() + stdout1.decode() + stderr1.decode()]

    return run


def LatexCompiler():
    def run(code):
        open("/tmp/a.tex", "w").write(code)
        output = os.popen("pdflatex /tmp/a.tex").read()
        return output

def ExtractCode(llm, keep_main=False, postfix=""):
    def run(orig_output):
        if keep_main:
            assert postfix == ""
            output = llm("Take the below answer to my programming question and return just the complete code in a single file so I can copy and paste it into an editor and directly run it. Include any header and main necessary so I can run it by copying this one file. Here is the code: \n" + orig_output)
        else:
            output = llm("Take the below answer to my programming question and return just the complete code in a single file so I can copy and paste it into an editor and directly run it. Remove any test cases. Remove any main function. I will write those myself. Do include header imports. Here is the code: \n" + orig_output + ("\nI will be running this code with the following helper functions:\n" + postfix if postfix else ""))

        print("DO EXTRACT")
        print("HAVE", output)
        output = output.replace("```python", "```")
        output = output.replace("```c", "```")
        output = output.replace("```rust", "```")
        output = output.replace("```sh", "```")
        if "```" in output:
            yield output.split("```")[1] + "\n" + postfix
            out1 = "\n".join(output.split("```")[1::2])
            #yield out1 + "\n" + postfix
        else:
            yield output + "\n" + postfix
            #yield orig_output + "\n" + postfix

    return run

class Node:
    def __init__(self, runner):
        self.runner = runner

    def __call__(self, orig_output):
        print("DO CALL", self.runner)
        return self.runner(orig_output)

    def __gt__(self, other_node):
        print("THENNODE", self, other_node)
        return ThenNode(self, other_node)

    def __rshift__(self, other_node):
        print("THENNODE", self, other_node)
        return ThenNode(self, other_node)
    
    def __and__(self, other_node):
        return AndNode(self, other_node)

    def __or__(self, other_node):
        return OrNode(self, other_node)

    def __invert__(self):
        return NotNode(self)
    
class ThenNode(Node):
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __call__(self, orig_output):
        for output1 in self.node1(orig_output):
            for output2 in self.node2(output1):
                yield output2

class AndNode(Node):
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            for output2, txt2 in self.node2(orig_output):
                yield output1 and output2, txt1 + "\n" + txt2

class OrNode(Node):
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

    def __call__(self, orig_output):
        for output1, txt1 in self.node1(orig_output):
            yield not output1, txt1

class PyEvaluator(Node):
    def __call__(self, x):
        return [self.runner(x)]
            

def ExtractJSON(llm):
    def run(orig_output):
        output = llm("Take the below answer to my question asking for a JSON output and just return the JSON obcject directly, with no other description, so I can copy it into an editor directly:\n" + orig_output)

        output = output.replace("```json", "```")
        if "```" in output:
            out1 = "\n".join(output.split("```")[1::2])
            yield out1
        else:
            yield output

    return run


def RustCompiler():
    pass


class SubstringEvaluator(Node):
    def __init__(self, substr):
        self.substr = substr

    def __call__(self, output):
        print(output)
        if self.substr in output:
            yield True, f"Substring {self.substr} found in output. Full log: {output}"
        else:
            yield False, f"Substring {self.substr} not found in output. Full log: {output}"



def JSONSubsetEvaluator(goal):
    def check(goal, output):
        if isinstance(goal, dict) and isinstance(output, dict):
            # Iterate over all key-value pairs in the goal dictionary
            for key, value in goal.items():
                # Check if the key is present in the output
                if key not in output:
                    return False
                # If the value is a dict or list, recursively check
                if isinstance(value, (dict, list)):
                    if not check(value, output[key]):
                        return False
                # Otherwise, check if the value matches
                elif output[key] != value:
                    return False
        elif isinstance(goal, list) and isinstance(output, list):
            # Check each element in the goal list
            for item in goal:
                if item not in output:
                    return False
        else:
            # Not a dict or list, so check if the values are equal
            return goal == output
    
        # todo better error message
        yield True, ""
        
    def evaluate(output):
        print("TRY", json.loads(output), goal)
        return check(goal, json.loads(output))
    return evaluate

def LLMEvaluator(llm, check_prompt):
    def evaluate(output):
        out = llm.yes_or_no(check_prompt.replace("<A>", output))
        # todo: make the reason better
        yield out, f"LLM says {out}"
    return evaluate

def LLMVisionRun(llm, check_prompt, check_image):
    def evaluate(output):
        print("RUN VISION")
        out = llm(check_prompt.replace("<A>", output), add_image=Image.open(check_image), max_tokens=128 )
        yield out
    return evaluate

def LLMRun(llm, check_prompt):
    def evaluate(output):
        print("^^^^^^^^^^^^")
        print("PASSING", check_prompt.replace("<A>", output))
        print("vvvvvvvvvvvvv")
        out = llm(check_prompt.replace("<A>", output))
        print("Got output", out)
        yield out
    return evaluate

class Conversation:
    def __init__(self, llm):
        self.llm = llm
        self.history = []

    def send_user(self, msg):
        self.history.append(msg)
        output = self.llm(self.history)
        self.history.append(output)
        return output

    def __repr__(self):
        return "Conversation(" + repr(self.history) + ")"
        

class TestCase:
    def __init__(self, llm):
        self.conversation = Conversation(llm)

    def run(self, prompt, debug=True):
        if 'pipeline' in dir(self):
            return self.run_pipeline(self.pipeline, prompt, debug)

        if 'setup' in dir(self):
            self.pipeline = self.setup()
            return self.run_pipeline(self.pipeline, prompt, debug)

        if debug:
            print("Running", prompt)
        fix_errors = iter(self.fix_errors)
        while True:
            output = self.conversation.send_user(prompt)
            if debug:
                print()
                print("Got output", output)

            outputs = []
            for option in self.apply_postproc(output, self.output_processors):
                if debug:
                    print("Postproc option:", option)
                outputs.append(option)
                if self.evaluate(prompt, option):
                    return True

            try:
                fix = next(fix_errors)
            except:
                return False

            # Try to fix whichever option we thought was most likely
            fix(self.conversation, outputs[0])
            if debug:
                print("Tried to fix the output with",
                      self.conversation)

    def apply_postproc(self, output, processors):
        outputs = [output]
        for postproc in processors:
            print("Do postproc", postproc)
            next_outputs = []
            for output in outputs:
                next_outputs.extend(postproc(output))
            outputs = next_outputs
            print("--"*40)
            for x in outputs:
                print(x)
                print("--"*40)
    
        return outputs

    def run_pipeline(self, node, prompt, debug=True):
        begin = self.conversation.send_user(prompt)
        
        for success, output in node(begin):
            if success:
                return True
            else:
                pass

        if 'fix_errors' in dir(self) and self.fix_errors:
            begin = self.fix_errors(self.conversation, output)

            print("Try again", self.conversation)
            for success, output in node(begin):
                if success:
                    return True
                else:
                    pass
            
        return False

    

def make_python_test(q_and_a, header=""):
    qs = []
    
    for q, a in q_and_a:
        qs.append(f"""
{header}

answer = {q}
expected = {a}
assert answer == expected, f'Wrong answer; got {{answer}} instead of {{expected}}'""")
    qs.append("print('All tests passed')")

    return "\n".join(qs), "All tests passed"
    

def make_c_test(q_and_a, header=""):
    qs = []

    qs.append("#include<stdio.h>\n#include<stdlib.h>\nint main() {");
    for q, a in q_and_a:
        qs.append(f"""
{header}

int answer = {q};
int expected = {a};
if (answer != expected) {{
    printf("Wrong answer; got %d instead of %d.\\n", answer, expected);
    exit(1);
}}""")
    qs.append('printf("All tests passed\\n");')

    qs.append("}");
    
    return "\n".join(qs), "All tests passed"
        
    

