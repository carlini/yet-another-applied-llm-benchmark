import subprocess
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
    conversation.send_user("I ran the code you suggested but got this wrong output: " + error_message + "\nPlease fix this error and then re-write the entire code block correctly this time.")


def PythonRun(test_case):
    def run(code):
        with open("/tmp/a.py", "w") as file:
            file.write(code + "\n\n" + test_case)

        # Running the Python script and capturing stdout and stderr
        process = subprocess.Popen(["python3", "/tmp/a.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Decoding from bytes to string and returning both
        return [stdout.decode() + stderr.decode()]

    return run


def LatexCompiler():
    def run(code):
        open("/tmp/a.tex", "w").write(code)
        output = os.popen("pdflatex /tmp/a.tex").read()
        return output

def ExtractCode(llm):
    def run(orig_output):
        output = llm("Take the below answer to my programming question and return just the complete code in a single file so I can copy and paste it into an editor and directly run it:\n" + orig_output)

        output = output.replace("```python", "```")
        if "```" in output:
            out1 = "\n".join(output.split("```")[1::2])
            yield out1
        else:
            yield orig_output

    return run

def ExtractJSON(llm):
    def run(orig_output):
        output = llm("Take the below answer to my question asking for a JSON output and just return the JSON obcject directly, with no other description, so I can copy it into an editor directly:\n" + orig_output)

        output = output.replace("```json", "```")
        if "```" in output:
            out1 = "\n".join(output.split("```")[1::2])
            yield out1
        else:
            yield orig_output

    return run


def RustCompiler():
    pass


def SubstringEvaluator(substr):
    def evaluate(prompt, output):
        return substr in output
    return evaluate

    
def JsonSubsetEvaluator(goal):
    def check(goal, output):
        if isinstance(goal, dict) and isinstance(output, dict):
            # Iterate over all key-value pairs in the goal dictionary
            for key, value in goal.items():
                # Check if the key is present in the output
                if key not in output:
                    print("Fail on", key)
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
    
        return True
        
    def evaluate(prompt, output):
        return check(goal, json.loads(output))
    return evaluate

def LLMEvaluator(llm, check_prompt):
    def evaluate(prompt, output):
        out = llm.yes_or_no(check_prompt.replace("<Q>", prompt).replace("<A>", output))
        print("GOT", out)
        return out
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
            print("Running", postproc)
            next_outputs = []
            for output in outputs:
                next_outputs.extend(postproc(output))
            outputs = next_outputs
            print("NEXT ITER", outputs)
    
        return outputs

def make_python_test(q_and_a):
    qs = []
    
    for q, a in q_and_a:
        qs.append(f"answer = {q}\nexpected = {a}\nassert answer == expected, f'Wrong answer; got {{answer}} instead of {{expected}}'")
    qs.append("print('All tests passed')")

    return "\n".join(qs), "All tests passed"
        
    
