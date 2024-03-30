from evaluator import *

DESCRIPTION = "This test checks is the model can figure out the user has put an accidental extra brace in the request body."

TAGS = ['explain', 'python']

question = """
Why isn't this working

```
@app.route('/getsimilar', methods=['GET'])
def getsimilar():
    print('args',request.args)
    positive = request.args.get('positive', '')
    positive = positive.split("##")

    negative = request.args.get('negative', '')
    negative = negative.split("##")

    keep_yes = [i for i,x in enumerate(titles) if x in positive]
    set1_yes = emb[keep_yes]

    keep_no = [i for i,x in enumerate(titles) if x in negative]
    set1_no = emb[keep_no]

    print("OK", len(set1_yes), len(set1_no))
```

I see

```
args ImmutableMultiDict([('positive', 'Title: Towards Evaluating the Robustness of Neural Networks\nAuthors: Nicholas Carlini; David Wagner'), ('negative', 'Title: On Evaluating Adversarial Robustness Authors: Nicholas Carlini; Anish Athalye; Nicolas Papernot; Wieland Brendel; Jonas Rauber; Dimitris Tsipras; Ian Goodfellow; Aleksander Madry; Alexey Kurakin}')])
OK 1 0
```

Why don't I see OK 1 1? Instead it just says OK 1 0. List exactly one reason explaining what's wrong and what one change would fix it.
"""

judge = "I asked a question about why some code was incorrect. The answer is \"because the input contains an extra curly brace }\". Does this student answer say that?\n\n<A>\n\nAnswer either 'The student passes' or 'The student fails'."

TestBrokenExtraBrace = question >> LLMRun() >> (LLMRun(judge, llm=EVAL_LLM) >> SubstringEvaluator("student passes"))

if __name__ == "__main__":
    print(run_test(TestBrokenExtraBrace))


