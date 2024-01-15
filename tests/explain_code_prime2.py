from evaluator import *

DESCRIPTION = "Test if the model can interpret a minified and obfuscated JavaScript function and explain its function."

TAGS = ['explain']

question = """
What does this code do

function z(){let e=[],n=[];for(let r=2;e.length<20;r++)(n=n.map(e=>e-1)).some(e=>0===e)?n=n.map((n,r)=>0===n?e[r]:n):(e.push(r),n.push(r));return e}console.log(z());
"""

TestExplainPrime2 = question >> LLMRun() >> LLMRun("I showed a student some code that calculates 20 primes. I then tested their understanding by asking them to explain it to me. I'm going to show you their answer, I want you to evaluate whether or not their answer says something to the effect of \"it calculates the first 20 primes\". Do not judge their reasonining, just tell me if they got it right. \n Student Answer: \"<A>\"\n\n Think out loud then answer either \"The student passes\" or \"The student fails\".", llm=EVAL_LLM) >> SubstringEvaluator("student passes")

if __name__ == "__main__":
    print(run_test(TestExplainPrime2))
