from evaluator import *

DESCRIPTION = "Test if the model can guide a user through resolving a merge conflict when merging two branches."

TAGS = ['bash', "git", "agent"]

question = """
You are in a git repository. I have two branches, main and some other one I forgot the name of. Merge the other branch into main.

On each round you should just give me just one command to type, I'll run it exactly as-is, and give you the exact output. I will not make any changes. So do not write any placholder text. I'll get started:

INPUT: `pwd`

OUTPUT: `/usr/src/app`

INPUT: `ls`

OUTPUT: `main.py a b`

Now your turn. What do you want to run? Do not explain yourself, just give me exactly one command. Start your response with INPUT:"""


def test_merge_conflict_resolved():
    import os
    try:
        return open("sum.py").read().strip() == "x + y" and open("b").read().strip() == "b"
    except:
        return False

    return success


def setup():
    import os
    print(os.popen("""
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    git config --global init.defaultBranch main
    echo "a" > sum.py
    echo "b" > b
    git init
    git add sum.py b
    git commit -a -m "Initial commit"
    git branch other
    git checkout other
    echo "x + y" > sum.py
    git add sum.py
    git commit -a -m "subtraction"
    git log
    git checkout main
    echo "x - y" > sum.py
    git add sum.py
    git commit -a -m "addition"
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


TestGitMergeConflict = Setup(setup) >> Echo() >> question >> UntilDone(PyEvaluator(test_merge_conflict_resolved), (LLMConversation(
) >> PyFunc(do_extract) >> TerminalRun() >> PyFunc(do_prepare)), max_iters=10) >> PyEvaluator(test_merge_conflict_resolved)

if __name__ == "__main__":
    print(run_test(TestGitMergeConflict))
