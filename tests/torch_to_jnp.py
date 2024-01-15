from evaluator import *

DESCRIPTION = "Test if the model can convert a torch neural network to a jax numpy model."

TAGS = ['code', 'python']

question = """
Convert the following PyTorch code to pure JAX. Do not use any other libraries.

```python
import torch

class MLP(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = torch.nn.Linear(input_size, hidden_size)
        self.linear2 = torch.nn.Linear(hidden_size, output_size)

    def __call__(self, x):
        x = self.linear1(x)
        x = torch.relu(x)
        x = self.linear2(x)
        return torch.nn.functional.softmax(x, dim=1)

model = MLP(10, 20, 30)
x = torch.randn(5, 10)
y = model(x)
print(list(y.flatten().numpy().sum(1)))
```
"""

TestTorchJnp = question >> LLMRun() >> ExtractCode(keep_main=True) >> \
    ((~SubstringEvaluator("import torch")) &
     (PythonRun() >> (SubstringEvaluator("1.0,") | SubstringEvaluator("1.00000") | SubstringEvaluator("1.0 ") | SubstringEvaluator("0.99999"))))



if __name__ == "__main__":
    print(run_test(TestTorchJnp))
