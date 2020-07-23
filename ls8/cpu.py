"""CPU functionality."""

import sys
import time
import code 


start_time = time.time()
print("start time", start_time)
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram=[0]*256
        self.register = [0] * 8
        self.register[7] = 0xf4 # Stack Pointer (initialized to f4)
        self.pc = 0
        self.sp = 7
        self.branchtable = {}
        self.running = True
        self.branchtable[0b00000001] = self.halt
        self.branchtable[0b10000010] = self.load_reg
        self.branchtable[0b01000111] = self.print_reg
        self.branchtable[0b10100010] = self.mult
        self.branchtable[0b10100000] = self.add
        self.branchtable[0b01000101] = self.push
        self.branchtable[0b01000110] = self.pop
        self.branchtable[0b01010000] = self.call_sub
        

    def push(self, reg_num, null):
        
        self.register[self.sp] -= 1 # Decrement stack pointer
        self.ram[self.register[self.sp]] = self.register[reg_num]

    def pop(self, reg, null):

        self.register[reg] = self.ram[self.register[self.sp]] 
        self.register[self.sp] +=1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def call_sub(self, operand_a, null):
        print("You called me")
        

    def ram_write(self, MDR, MAR):
        try:
            self.ram[MAR] = MDR
            return True
        except:
            return False

    def load_reg(self, op_a, op_b):
        self.register[int(format(op_a, '08b')[-3:])] = op_b

    def print_reg(self, op_a, null):
        print(f"Value in register {op_a}: {self.register[op_a]}")

    def mult(self, op_a, op_b):
        self.alu('MUL', op_a, op_b)

    def add(self, op_a, op_b):
        self.alu("ADD", op_a, op_b)


    def load(self, argv=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        try: # Why is this try except block not working?
            if argv is None:
                argv = sys.argv[1]
            print("sys", argv)
            with open(argv) as f:
                program.clear()
                for line in f:
                    line = line.split("#")[0] # wrap inside int() when all input is right type
                    line = line.strip()
                    # print(line)
                    if line == "":
                        continue
                    line = int(line, 2)
                    # print(repr("{0:b}".format(line)))
                    program.append(line)
        except IndexError:
            print("Please enter a filepath")
            sys.exit(1)
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]} or path not entered")
            sys.exit(1)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        elif op=="MUL":
            self.register[reg_a] *= self.register[reg_b] 
        else:
            raise Exception("Unsupported ALU operation")


    def halt(self, _, __):
        self.running = False
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
        # Set up the operands and increment the pc

        
        # Run the instructions
        while self.running:

            if self.pc > len(self.ram)-3: ## safeguard. May not be necessary. HAVE TO USE format() NOT bin() or gets messed up. 
                print("Stack Overflow! Program Terminated")
                break

            IR = self.ram[self.pc]
            operand_a = self.ram[self.pc+1]; operand_b = self.ram[self.pc+2]; # print("IR", IR, "operand A/B", operand_a, operand_b)
            a = format(IR, '08b')[:2]; b = format(IR, '08b')[2:3]; c = format(IR, '08b')[2:][3:4]; d = format(IR, '08b')[2:][4:]
            # print(f"a: {a}, b: {b}, c: {c}, d: {d}")
            number_operands = (IR & 0b11000000) >> 6

            # self.pc += int(a,2) + 1 # Naive implementation
            self.pc += number_operands + 1

            use_branch_table = True
            if use_branch_table == True:
                try:
                    self.branchtable[IR](operand_a, operand_b)
                except:
                    print(f"Instruction {IR} not found. Exiting with code 1")
                    # sys.exit(1)
            else:
                # O(n) performance. 
                if IR == 0b00000001:
                    running = False 
                    print("Halted")
                elif IR == 0b10000010: # LDI register immediate
                    self.register[int(format(operand_a, '08b')[-3:])] = operand_b
                    # print("register", self.register)
                elif IR == 0b01000111: # Print value of register in operand a
                    print(f"Value in register {operand_a}: {self.register[operand_a]}")
                elif IR == 0b10100010: # multiply registers addressed as opearnds A and B - stores in register of op a
                    # bytecode[IR]("MUL", operand_a, operand_b)
                    self.alu('MUL', operand_a, operand_b)
                elif IR == 0b10100000: # Add Registers opA and opB
                    self.alu("ADD", operand_a, operand_b)



end_time = time.time()
print("Total Time = ", (end_time - start_time)*1000000, " Milliseconds")


if __name__ == "__main__":
        
    cpu = CPU()
    print(cpu.ram_read(4))
    cpu.ram_write(5,4)
    print(cpu.ram_read(4))
    cpu.run()
    code.interact(local=globals())
    # while True:
    #     x = input("Enter a command: ")
    #     if x == 'q':
    #         quit()
    #     try:
    #         x
    #     except:
    #         print("error")