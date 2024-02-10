from evaluator import *

DESCRIPTION = "Test if the model can guide a user through a series of git commands to identify and cherrypick a specific commit from a branch onto the main branch."

TAGS = ['bash', "git", "agent"]


question = """
You are in a git repository. I have two branches, main and some other one I forgot the name of. Take just the first commit that differs between main and the other branch, and commit it onto main.

On each round you should just give me just one command to type, I'll run it exactly as-is, and give you the exact output. I will not make any changes. So do not write any placholder text. I'll get started:

INPUT: `pwd`

OUTPUT: `/usr/src/app`

INPUT: `ls`

OUTPUT: `main.py a b`

Now your turn. What do you want to run? Do not explain yourself, just give me exactly one command. Start your response with INPUT:"""


def test_ok():
    import os
    try:
        return open("e").read().strip() == "e" and not os.path.exists("d") and open("c").read().strip() == "c"
    except:
        return False
    
    return success

def setup():
    import os
    print(os.popen("""
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    git config --global init.defaultBranch main
    echo "a" > a
    echo "b" > b
    git init
    git add a b
    git commit -a -m "Initial commit"
    git branch other
    git checkout other
    echo "c" > c
    git add c
    git commit -a -m "Add c"
    echo "d" > d
    git add d
    git commit -a -m "Add d"
    git log
    git checkout main
    echo "e" > e
    git add e
    git commit -a -m "Add e"
    git log
    """).read())

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
    return f"I get an OUTPUT: `{x}`.\n\nWhat is the exact command I should run next? Start your response with INPUT:"
    
TestGitCherrypick = Setup(setup) >> Echo() >> question >> UntilDone(PyEvaluator(test_ok), (LLMConversation() >> PyFunc(do_extract) >> TerminalRun() >> PyFunc(do_prepare)), max_iters=6) >> PyEvaluator(test_ok)
    

if __name__ == "__main__":
    print(run_test(TestGitCherrypick))
