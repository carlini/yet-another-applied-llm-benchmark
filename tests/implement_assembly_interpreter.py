from evaluator import *

DESCRIPTION = "Test if the model can implement an interpreter for a new assembly language from a text description."

TAGS = ['code', 'python']

question = """Here is the description of a new assembly language:

* 8 registers (R1, R2, R3, R4, R5, R6, R7, R8) that can hold integers.
* 1 flag that can hold a boolean value (True or False).
* 100 memory addresses (0-99) that can hold integers.
* 1 instruction pointer that points to the current instruction being executed.

Each instruction is of the form
OP ARG1 ARG2 ...
where ARGn can be either a register (e.g., R1) or a constant (e.g., 10).

Labels are written with a lowercase word followed by colon.

The assembly language supports the following instructions:
* SET Rx C: Assigns the value C to register Rx.
* ADD Rx Ry Rz: Adds the values of Ry and Rz and stores the result in Rx.
* (similarly for SUB, MUL, DIV, MOD)
* EQ Rx Ry: Sets the flag to True if Rx and Ry are equal, False otherwise.
* (similarly for NEQ, LT (Rx < Ry), LTE, GT, GTE)
* INC/DEC Rx: Increments/Decrements the value of Rx by one.
* JMP L: Jumps to label L unconditionally.
* JT/JF (jump if true / jump if false) L: Jumps to label L if the is set or not set.
* LOAD Rx M: Loads the value at memory address M into register Rx.
* STORE Rx M: Stores the value of register Rx into memory address M.
* HCF: Stops the program (with pizzazz)

For example here is a program to compute the first 20 square numbers (1, 4, 9, 16, 25, ...):

    SET R1 0      // Counter for storing squares
    SET R2 1      // Number to square

loop:
    MUL R3 R2 R2  // R3 = R2 * R2
    STORE R3 R1   // Store R3 at address R1
    INC R1        // Increment address
    INC R2        // Increment number
    SET R3 20
    EQ R1 R3      // Check if 20 squares are found
    JF loop       // If not 20 squares found yet, continue finding

end:
    HCF           // Stop program


Write me a python interpreter `evaluate(str)` that returns the resulting memory state after running the program. For example, `evaluate(program)` should return `[1, 4, 9, 16, 25, ...]` for the above program.
"""

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

test_case, answer = make_python_test([(f'evaluate("""{code}""")[:10]', "[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]"),
                                      (f'evaluate("""{primes}""")[:10]', "[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]")
                                      ])

TestImplementAssembly = question >> LLMRun() >> ExtractCode(lang="python") >> PythonRun(test_case) >> SubstringEvaluator(answer)


if __name__ == "__main__":
    print(run_test(TestImplementAssembly))

    
