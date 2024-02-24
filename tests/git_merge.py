from evaluator import *

DESCRIPTION = "Test if the model can guide a user through a series of git commands to merge a specific branch into the main branch."

TAGS = ['bash', "git", "agent"]

question = """
You are in a git repository. I have two branches, main and some other one I forgot the name of. Merge the other branch into main.

On each round you should just give me just one command to type, I'll run it exactly as-is, and give you the exact output. I will not make any changes. So do not write any placholder text. I'll get started:

INPUT: `pwd`

OUTPUT: `/usr/src/app`

INPUT: `ls`

OUTPUT: `main.py a b`

Now your turn. What do you want to run? Do not explain yourself, just give me exactly one command. Start your response with INPUT:"""


def test_ok_merge():
    try:
        math_content = open("math.py").read().strip()
        readme_content = open("README.md").read().strip()
        mul_content = open("mul.py").read().strip()

        return (
            math_content == "x + y\nx - y"
            and readme_content == "A repo about something\nYou run it like this"
            and mul_content == "x * y"
        )
    except:
        return False


def test_merge_conflict_resolved():
    import os
    try:
        return open("sum.py").read().strip() == "x + y" and open("b").read().strip() == "b"
    except:
        return False


def setup_merge():
    import os
    print(os.popen("""
    git config --global user.name "Your Name"
    git config --global user.email "you@example.com"
    git config --global init.defaultBranch main
    echo "x + y" > math.py
    echo "A repo about something" > README.md
    git init
    git add math.py README.md
    git commit -a -m "Initial commit"
    git branch other
    git checkout other
    echo "x + y\nx - y" > math.py
    git add math.py
    git commit -a -m "Subtraction"
    echo "A repo about something\nYou run it like this" > README.md
    git add README.md
    git commit -a -m "README"
    git log
    git checkout main
    echo "x * y" > mul.py
    git add mul.py
    git commit -a -m "Multiplication"
    git log
    """).read())


def setup_merge_conflict():
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
    git commit -a -m "addition"
    git log
    git checkout main
    echo "x - y" > sum.py
    git add sum.py
    git commit -a -m "subtraction"
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


TestGitMerge = Setup(setup_merge) >> Echo() >> question >> UntilDone(PyEvaluator(test_ok_merge), (LLMConversation(
) >> PyFunc(do_extract) >> TerminalRun() >> PyFunc(do_prepare)), max_iters=6) >> PyEvaluator(test_ok_merge)

TestGitMergeConflict = Setup(setup_merge_conflict) >> Echo() >> question >> UntilDone(PyEvaluator(test_merge_conflict_resolved), (LLMConversation(
) >> PyFunc(do_extract) >> TerminalRun() >> PyFunc(do_prepare)), max_iters=10) >> PyEvaluator(test_merge_conflict_resolved)

if __name__ == "__main__":
    print(run_test(TestGitMerge))
    print(run_test(TestGitMergeConflict))
