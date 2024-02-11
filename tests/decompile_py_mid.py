from evaluator import *

DESCRIPTION = "Test if the model can disassemble Python bytecode and create a function that returns a list of prime numbers and their negations."

TAGS = ['code', 'python']

question = """
Disassemble the following python into a function called foo:

  5           0 BUILD_LIST               0
              2 STORE_FAST               1 (primes)

  6           4 LOAD_GLOBAL              0 (range)
              6 LOAD_CONST               1 (2)
              8 LOAD_FAST                0 (max_number)
             10 LOAD_CONST               2 (1)
             12 BINARY_ADD
             14 CALL_FUNCTION            2
             16 GET_ITER
        >>   18 FOR_ITER                94 (to 114)
             20 STORE_FAST               2 (possible_prime)

  7          22 LOAD_CONST               3 (True)
             24 STORE_FAST               3 (is_prime)

  9          26 LOAD_GLOBAL              0 (range)
             28 LOAD_CONST               1 (2)
             30 LOAD_GLOBAL              1 (int)
             32 LOAD_FAST                2 (possible_prime)
             34 LOAD_CONST               4 (0.5)
             36 BINARY_POWER
             38 CALL_FUNCTION            1
             40 LOAD_CONST               2 (1)
             42 BINARY_ADD
             44 CALL_FUNCTION            2
             46 GET_ITER
        >>   48 FOR_ITER                24 (to 74)
             50 STORE_FAST               4 (num)

 10          52 LOAD_FAST                2 (possible_prime)
             54 LOAD_FAST                4 (num)
             56 BINARY_MODULO
             58 LOAD_CONST               5 (0)
             60 COMPARE_OP               2 (==)
             62 POP_JUMP_IF_FALSE       48

 11          64 LOAD_CONST               6 (False)
             66 STORE_FAST               3 (is_prime)

 12          68 POP_TOP
             70 JUMP_ABSOLUTE           74
             72 JUMP_ABSOLUTE           48

 13     >>   74 LOAD_FAST                3 (is_prime)
             76 POP_JUMP_IF_FALSE       18

 14          78 LOAD_FAST                1 (primes)
             80 LOAD_METHOD              2 (append)
             82 LOAD_FAST                2 (possible_prime)
             84 CALL_METHOD              1
             86 POP_TOP

 16          88 LOAD_FAST                2 (possible_prime)
             90 LOAD_CONST               1 (2)
             92 BINARY_MODULO
             94 LOAD_CONST               5 (0)
             96 COMPARE_OP               3 (!=)
             98 POP_JUMP_IF_FALSE       18

 17         100 LOAD_FAST                1 (primes)
            102 LOAD_METHOD              2 (append)
            104 LOAD_FAST                2 (possible_prime)
            106 UNARY_NEGATIVE
            108 CALL_METHOD              1
            110 POP_TOP
            112 JUMP_ABSOLUTE           18

 18     >>  114 LOAD_FAST                1 (primes)
            116 RETURN_VALUE

"""

test_case, answer = make_python_test([("foo(20)", "[2, 3, -3, 5, -5, 7, -7, 11, -11, 13, -13, 17, -17, 19, -19]")])


TestDisasPrimes = question >> LLMRun() >> ExtractCode(keep_main=False) >> PythonRun(test_case) >> SubstringEvaluator(answer)

if __name__ == "__main__":
    print(run_test(TestDisasPrimes))
