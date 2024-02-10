from evaluator import *

DESCRIPTION = "Test if the model can guide a user in a conversation to setup a git repo."

TAGS = ['bash', "git", "agent"]

question = """
You are in a repository with two files `a` and `b`. Make a new git repo and then commit them both.

On each round you should just give me just one command to type, I'll run it, and give you the exact output. I'll get started:

INPUT: `pwd`

OUTPUT: `/usr/src/app`

INPUT: `ls`

OUTPUT: `main.py a b`

Now your turn. What do you want to run? Do not explain yourself, just give me exactly one command. Start your response with INPUT:"""


def test_ok():
    import os
    success = os.popen("git rev-list --all --count").read().strip() == "1"
    return success

def setup():
    import os
    open("a", "w").write("a")
    open("b", "w").write("b")
    os.popen('git config --global user.email "you@example.com"').read()
    os.popen('git config --global user.name "Your Name"').read()

def do_extract(x):
    if 'INPUT:' in x:
        x = x.split("INPUT:")[1]
    try:
        to_send = x.split("`")[1]
    except:
        to_send = x.split("\n")[0]
    return to_send

def do_prepare(x):
    print("Preparing to pass back", x)
    return f"OUTPUT: `{x}`.\n\nWhat command should I run next? Start your response with INPUT:"
    
TestGitSimple = Setup(setup) >> question >> UntilDone(PyEvaluator(test_ok), (LLMConversation() >> PyFunc(do_extract) >> TerminalRun() >> PyFunc(do_prepare)), max_iters=4) >> PyEvaluator(test_ok)
    

if __name__ == "__main__":
    print(run_test(TestGitSimple))
