from evaluator import *

DESCRIPTION = "Test if a model correctly understands how advanced indexing works in numpy."

TAGS = ['explain', 'python']

question = """
What will this program print:

```python
import numpy as np

array = np.zeros((10, 20, 30))
idxs = [1, 2, 3]

print("The array shape is", array[0, :, idxs].shape)
```
"""

TestNumpyAdvancedIndex = question >> LLMRun() >> SubstringEvaluator("The array shape is (3, 20)")

question = """
Consider this program

```python
import numpy as np

array = np.zeros((10, 20, 30))
idxs = [1, 2, 3]

print("The first array shape is", array[0][:, idxs].shape)
print("The second array shape is", array[0, :, idxs].shape)
```

Tell me what this program will print, and then explain why the two print statements don't print the same thing
"""

TestNumpyAdvancedIndexEasier = question >> LLMRun() >> (SubstringEvaluator("(3, 20)") & SubstringEvaluator("(20, 3)") & SubstringEvaluator("dvanced indexing"))

if __name__ == "__main__":
    print(run_test(TestNumpyAdvancedIndexEasier))
