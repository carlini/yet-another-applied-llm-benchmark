from evaluator import *

DESCRIPTION = "Test if the model can correctly convert a list of indexes to a one-hot vector in Python using JAX."

TAGS = ['code', 'python']

question = """
I have list of indexes and I want to convert it to one hot vector using jax and the function should be jittable and the function should be jitted. name the function one_hot and it should get two arguments the first one is the indexes and the second one is the number of possible labeles. Just give me the code
"""

test_case, answer = make_python_test([("str(one_hot(jnp.array([1,2,0]),5))","str(jnp.array([[0.0,1.0,0.0,0.0,0.0],[0.0,0.0,1.0,0.0,0.0],[1.0,0.0,0.0,0.0,0.0]]))")],header='import jax.numpy as jnp')




TestJaxOneHot = question >> LLMRun() >> ExtractCode() >> Echo() >>  PythonRun(test_case) >>  Echo() >> SubstringEvaluator(answer)
                                                                    

if __name__ == "__main__":
    print(run_test(TestJaxOneHot))
