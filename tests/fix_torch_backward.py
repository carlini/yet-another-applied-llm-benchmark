from evaluator import *

DESCRIPTION = "Test if the model can fix and explain a bug in PyTorch code related to forgetting to zero gradients."

TAGS = ['code', 'python', 'fix']

code = """
```
import torch
import torch.nn as nn
import torch.optim as optim

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc = nn.Linear(1, 1)

    def forward(self, x):
        return self.fc(x)

def PGD(model, input, target, loss_fn, epsilon, alpha, num_iter):
    perturbation = torch.zeros_like(input, requires_grad=True)

    for i in range(num_iter):
        output = model(input + perturbation)
        loss = loss_fn(output, target)

        loss.backward()

        # Update perturbation
        perturbation_grad = perturbation.grad.data
        perturbation.data = perturbation.data + alpha * perturbation_grad.sign()
        perturbation.data = torch.clamp(perturbation.data, -epsilon, epsilon)
        perturbation.grad.data.zero_()

    return input + perturbation

model = SimpleNet()

input = torch.tensor([[1.0]], requires_grad=True)
target = torch.tensor([[2.0]])

loss_fn = nn.MSELoss()

epsilon = 0.1
alpha = 0.01
num_iter = 2

adversarial_input = PGD(model, input, target, loss_fn, epsilon, alpha, num_iter)
print("Resulting advex", adversarial_input)
```
"""

q1 = f"Fix the bug in this code. Rewrite the entire code exactly as-is but just fix any bugs.\n\n{code}"

TestTorchBackwardFix = q1 >> LLMRun() >> ExtractCode(keep_main=True) >> PythonRun() >> (SubstringEvaluator("tensor") & SubstringEvaluator("grad_fn=<Add"))

q2 = f"Explain the bug in this code.\n\n{code}"

TestTorchBackwardExplain = q2 >> LLMRun() >> LLMRun("Below is a student's explanation for a bug in a torch function.\n<A>\nDoes the student's answer say specifically \"the bug is caused by not zeroing the gradient in the backward pass\"? Think out loud and then finally answer either \"The student passes\" or \"The student fails\".", llm=EVAL_LLM) >> Echo() >> SubstringEvaluator("The student passes")


if __name__ == "__main__":
    print(run_test(TestTorchBackwardExplain))

