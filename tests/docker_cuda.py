from evaluator import *

DESCRIPTION = "This test case checks if the model can debug a docker cuda error"

TAGS = ['explain']

question = """
nicholas@server:~/project$ sudo docker start myproject
[sudo] password for nicholas: 
Error response from daemon: could not select device driver "" with capabilities: [[gpu]]
Error: failed to start containers: myproject
"""

TestFixDockerCuda = question >> LLMRun() >> (SubstringEvaluator("nvidia-container-toolkit") | SubstringEvaluator("nvidia-docker2"))

if __name__ == "__main__":
    print(run_test(TestFixDockerCuda))
