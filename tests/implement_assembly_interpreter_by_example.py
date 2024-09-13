from evaluator import *

DESCRIPTION = "Test if the model can implement an interpreter for a new assembly language given an example."

TAGS = ['code', 'python']

primes = """

SET R1 2          // Starting number to check for prime

start_find_primes:

    JMP is_prime // Control will return after executing is_prime with R1 as input and R2 containing the result

ready_prime:
    SET R7 1
    EQ R2 R7        // Check if R2 is 1 (prime)
    JF increment  // If not prime, skip storing and increment the number

    // Store prime number in memory and increment count
    STORE R1 R8   // Store prime number at address pointed by R8
    INC R8        // Increment prime count

    // Check if 100 primes are found
    SET R7 100
    EQ R8 R7
    JF increment  // If not 100 primes found yet, continue finding

    JMP end        // If 100 primes found, end program

increment:
    INC R1         // Increment number to check for prime
    JMP start_find_primes // Check next number

is_prime:
    SET R2 1       // Assume number is prime initially
    SET R3 2       // Start divisor from 2

start_loop:        // Label to start the loop
    // Check if we have exceeded the square root of R1
    MUL R4 R3 R3   // R4 = R3 * R3
    GT R4 R1       // Set flag if R4 > R1
    JT is_prime_end        // If not exceeded, continue; else, end loop

    MOD R6 R1 R3   // R6 = R1 % R3
    SET R7 0
    EQ R7 R6     // Check if R6 is 0
    JT not_prime   // If yes, number is not prime

    INC R3         // Increment divisor
    JMP start_loop // Repeat loop

not_prime:
    SET R2 0       // Set result to 0 (not prime)

is_prime_end:
    JMP ready_prime

end:
"""

code = """
    SET R1 0
    SET R2 1
loop:
    MUL R3 R2 R2
    STORE R3 R1
    INC R1
    INC R2
    SET R3 20
    EQ R1 R3
    JF loop
"""

question = f"""Here is an example program from a new assmebly language I made up that computes primes:

```
{primes}
```

ite me a python interpreter `evaluate(str)` that returns the resulting memory state after running the program. For example, `evaluate(program)` should return `[2, 3, 5, 7, ...]` for the above program.
"""


test_case, answer = make_python_test([(f'evaluate("""{code}""")[:10]', "[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]"),
                                      (f'evaluate("""{primes}""")[:10]', "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]")
                                      ])

TestImplementAssemblyByExample = question >> LLMRun() >> ExtractCode(lang="python") >> Echo() >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestImplementAssemblyByExample))

    
