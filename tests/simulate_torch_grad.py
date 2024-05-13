from evaluator import *

DESCRIPTION = "This test case checks if the model can predict what the gradient of a variable is in PyTorch."

TAGS = ['explain', 'python']

question = """
What will this function print

```
def diff_round(x, decimals=1):
    scale_factor = (10 ** decimals)
    x = x * scale_factor
    diff = (1 + 1e-2) * x - torch.floor(x)
    x = x - diff + (torch.floor(x) + torch.where(diff >= 0.5, 1, 0))
    x = x / scale_factor
    return x

g = torch.tensor([.99, 1.54, 1.9], dtype=torch.float32, requires_grad=True)
loss = torch.sum(diff_round(g, 1))
loss.backward()
print(g.grad.sum())
```
"""

TestSimTorchGrad = question >> LLMRun() >> SubstringEvaluator("-0.03")

if __name__ == "__main__":
    print(run_test(TestSimTorchGrad))

