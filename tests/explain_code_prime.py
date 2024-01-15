from evaluator import *

DESCRIPTION = "Test if the model can interpret a minified JavaScript function and explain its function."

TAGS = ['code', 'explain']

question = """
What does this code do

function q(e){if(e<=1)return!1;if(e<=3)return!0;if(e%2==0||e%3==0)return!1;for(let r=5;r*r<=e;r+=6)if(e%r==0||e%(r+2)==0)return!1;return!0}function z(){const e=[];let r=2;for(;e.length<20;)q(r)&&e.push(r),r++;return e.reverse(),e.reverse(),e}console.log(z());
"""

TestExplainPrime = question >> LLMRun() >> LLMRun("I showed a student some code that calculates 20 primes. I then tested their understanding by asking them to explain it to me. I'm going to show you their answer, I want you to evaluate whether or not their answer says something to the effect of \"it calculates the first 20 primes\". Do not judge their reasonining, just tell me if they got it right. \n Student Answer: \"<A>\"\n\n Think out loud then answer either \"The student passes\" or \"The student fails\".", llm=EVAL_LLM) >> SubstringEvaluator("student passes")

if __name__ == "__main__":
    print(run_test(TestExplainPrime))
