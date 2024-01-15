from evaluator import *

DESCRIPTION = "Test if the model can write a program in a new assembly language. This ability to learn a new language on-the-fly is important for many tasks."

TAGS = ['code']

class AssemblyEmulator:
    def __init__(self, instructions):
        self.registers = {"R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0, "R7": 0, "R8": 0}
        self.memory = [0] * 100
        self.instruction_pointer = 0
        self.instructions = instructions.split("\n")
        self.flag = False
        print(instructions)

    def run(self):

        def lookup(register_or_const):
            if register_or_const.startswith('R'):
                return self.registers[register_or_const]
            else:
                return int(register_or_const)

        bin_op = {
            "ADD": lambda a, b: a + b,
            "SUB": lambda a, b: a - b,
            "MUL": lambda a, b: a * b,
            "DIV": lambda a, b: a // b,
            "MOD": lambda a, b: a % b,
            }
        cmp_op = {
            "EQ": lambda a, b: a == b,
            "NEQ": lambda a, b: a != b,
            "LT": lambda a, b: a < b,
            "LTE": lambda a, b: a <= b,
            "GT": lambda a, b: a > b,
            "GTE": lambda a, b: a >= b,
            }
            
            
        ctr = 0
        while self.instruction_pointer < len(self.instructions):
            ctr += 1
            if ctr > 1e6:
                raise Exception("Infinite loop detected")

            parts = self.instructions[self.instruction_pointer].split("//")[0].replace(",","").split()
            if len(parts) == 0:
                self.instruction_pointer += 1
                continue

            instruction, args = parts[0], parts[1:]

            if instruction == "SET":
                self.registers[args[0]] = lookup(args[1])
            elif instruction in bin_op:
                self.registers[args[0]] = bin_op[instruction](lookup(args[1]), lookup(args[2]))
            elif instruction in cmp_op:
                self.flag = cmp_op[instruction](lookup(args[0]), lookup(args[1]))
            elif instruction == "INC":
                self.registers[args[0]] += 1
            elif instruction == "DEC":
                self.registers[args[0]] -= 1
            elif instruction == "JT" and self.flag:
                self.instruction_pointer = self.find_label(args[0])
                continue
            elif instruction == "JF" and not self.flag:
                self.instruction_pointer = self.find_label(args[0])
                continue
            elif instruction == "JMP":
                self.instruction_pointer = self.find_label(args[0])
                continue
            elif instruction == "LOAD":
                self.memory[lookup(args[1])] = lookup(args[0])
            elif instruction == "STORE":
                self.memory[lookup(args[1])] = lookup(args[0])
            elif instruction == "HCF":
                return

            self.instruction_pointer += 1

    def find_label(self, label):
        return next(i for i, instruction in enumerate(self.instructions) if instruction.strip().startswith(label + ':'))

    
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

Given this assembly language, write a program that {}"""

def expect(answer):
    def evaluate(code):
        try:
            emulator = AssemblyEmulator(code)
            emulator.run()
        except Exception as e:
            print("EXCEPTION", e)
            return False, str(e)
            
        return answer(emulator.memory), ""
    return evaluate

TestNewAssemblySquareNumbers = question.format("puts the first 20 square (1, 4, 9...) numbers in memory cells 0..19") >> LLMRun() >> ExtractCode(lang="a new assembly language I just made up") >> PyFunc(expect(lambda m: m[:20] == [i*i for i in range(1,21)]))

TestNewAssemblyPrimeNumbers = question.format("puts the first 20 prime numbers in memory cells 0..19") >> LLMRun() >> ExtractCode(lang="a new assembly language I just made up") >> PyFunc(expect(lambda m: m[:20] == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]))


if __name__ == "__main__":
    print(run_test(TestNewAssemblySquareNumbers))

    
