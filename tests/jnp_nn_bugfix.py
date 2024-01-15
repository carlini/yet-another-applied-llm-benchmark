from evaluator import *

DESCRIPTION = "Test if the model can identify and fix a bug in a given jax.numpy function."

TAGS = ['code', 'python']

question = """
Fix the bug in this jnp function. Write out the full correct version of the code.

import jax
import jax.numpy as jnp

def init_mlp_params(input_size, hidden_size, output_size, key):
    k1, k2 = jax.random.split(key)
    # Initialize weights and biases for the first linear layer
    w1 = jax.random.normal(k1, (hidden_size, input_size)) * jnp.sqrt(2.0 / input_size)
    b1 = jnp.zeros(hidden_size)
    # Initialize weights and biases for the second linear layer
    w2 = jax.random.normal(k2, (output_size, hidden_size)) * jnp.sqrt(2.0 / hidden_size)
    b2 = jnp.zeros(output_size)
    return {'w1': w1, 'b1': b1, 'w2': w2, 'b2': b2}

def mlp_apply(params, x):
    # First linear layer
    x = jnp.dot(x, params['w1'].T) + params['b1']
    # Relu activation
    x = jax.nn.relu(x)
    # Second linear layer
    x = jnp.dot(x, params['w2'].T) + params['b2']
    # Softmax activation
    return jax.nn.softmax(x, axis=1)

# Example usage:
key = jax.random.PRNGKey(0)
params = init_mlp_params(10, 20, 30, key)
x = jax.random.normal(key, (5, 10)) # random input similar to torch.randn
y = mlp_apply(params, x)
print(list(y.flatten().sum(1)))  # The output sum should be very close to [1, 1, 1, 1, 1]
"""

TestFixJnpBug = question >> LLMRun() >> ExtractCode(keep_main=True) >> \
    (PythonRun() >> (SubstringEvaluator("1.0,") | SubstringEvaluator("1.00000") | SubstringEvaluator("1.0 ") | SubstringEvaluator("0.99999")))



if __name__ == "__main__":
    print(run_test(TestFixJnpBug))
