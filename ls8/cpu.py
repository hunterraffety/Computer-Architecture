'''
    LDI: load "immediate", store a value in a register, or "set this register to this value".
    PRN: a pseudo-instruction that prints the numeric value stored in a register.
    HLT: halt the CPU and exit the emulator.
'''

'''
10000010 # LDI R0,8
00000000
00001000
01000111 # PRN R0
00000000
00000001 # HLT
'''

LDI = 0b10000010 # LDI R0,8 "Load Immediately"
NOP = 0b00000000 # "No Operation"
# don't know what this is. 0b00001000
PRN = 0b01000111 # PRN R0 "Print"
# same as NOP 0b00000000
HLT = 0b00000001 # HLT "Halt"

"""CPU functionality."""

import sys
print(sys.argv)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {} #  our '256' bytes of memory storage
        self.reg = [0] * 8 # 8 general purpose registers
        self.pc = 0  # program counter, index into memory of the current instruction
        self.running = True # moves running into class constructor

    def load(self):
        """Load a program into memory."""

        address = 0

        program = sys.argv[1] # takes in argument when executing file.

        # throw back thursday
        with open(program) as p:
            for line in p:
                l = line.split("#")
                print(f"l: {l}") 
                print(f"l[0]: {l[0]}") # checking first item
                l[0] = l[0].strip() # removes whitespace from line with strip()
                print(f"l[0].strip(): {l[0].strip()}")
                if l[0] is "":
                    continue
                
                instruction = int(l[0], 2) # grabs the binary from the line, ensures numbers, ensures base 2
                self.ram_write(address, instruction)
                address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8 - 130
        #     0b00000000,
        #     0b00001000, # - 8
        #     0b01000111, # PRN R0 # 71
        #     0b00000000,
        #     0b00000001, # HLT - 1
        # ]

        for instruction in program:
            self.ram[address] = instruction # ram_write method
            address += 1 # counter bump

    def ram_read(self, address): # should accept the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, address, instruction): # should accept a value to write, and the address to write it to.
        self.ram[address] = instruction

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        if op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            instruction = self.ram_read(self.pc) # sets current instruction by invoking ram_read method and passing count as param. Looks in the ram dict to grab the current instruction as referenced by the pc count.
            print(instruction)
        # Step 4: Implement the HLT instruction handler
        # Add the HLT instruction definition to cpu.py so that you can refer to it by name instead of by numeric value.
        # In run() in your switch, exit the loop if a HLT instruction is encountered, regardless of whether or not there are more lines of code in the LS-8 program you loaded.
            if instruction is HLT:
                running = False
                self.pc += 1
            # We can consider HLT to be similar to Python's exit() in that we stop whatever we are doing, wherever we are.
            
            # Step 5: Add the LDI instruction
            # This instruction sets a specified register to a specified value.
            # See the LS-8 spec for the details of what this instruction does and its opcode value.
            elif instruction is LDI:
                register_number = self.reg[self.pc + 1] # operand A
                self.reg[register_number] = self.ram[self.pc + 2] # operand B
                self.pc += 3 # 3 steps PC ^^

            # Step 6: Add the PRN instruction
            # This is a very similar process to adding LDI, but the handler is simpler. See the LS-8 spec.
            # At this point, you should be able to run the program and have it print 8 to the console!
            elif instruction is PRN:
                idx = self.ram[self.pc + 1] # operand A
                register_number = self.reg[self.pc + 1] # I am not sure what this does. I did it in LDI too.
                self.pc += 2 # 2 step PC ^^

            else:
                print(f"Unknown instruction at index {self.pc}")
                sys.exit(1)
"""
base 10, decimal: 0-9
base 2, binary: 0, 1
base 16, hex: 0-9, a-f

dec: 33
binary: 100001
00000011 = 3
00101010 = 42
128, 64, 32, 16, 8, 4, 2, 1 etc.

nybbles = 4bit blocks
"""