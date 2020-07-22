"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram=[0]*256
        self.register = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]


    def ram_write(self, MDR, MAR):
        try:
            self.ram[MAR] = MDR
            return True
        except:
            return False


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        
        with open(sys.argv[1]) as f:
            for line in f:
                line = line.split("#")[0] # wrap inside int() when all input is right type
                line = line.strip()
                # print(line)
                if line == "":
                    continue
                line = int(line, 2)
                print(repr("{0:b}".format(line)))

        sys.exit(0)


        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        # program = sys.argv[1]
        # print("sys.argv[1]", program)


        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        # Set up the operands and increment the pc

        
        # Run the instructions
        running = True
        while running:

            if self.pc > len(self.ram)-3: ## safeguard. May not be necessary. HAVE TO USE format() NOT bin() or gets messed up. 
                print("Stack Overflow! Program Terminated")
                break


            IR = self.ram[self.pc]
            operand_a = self.ram[self.pc+1]; operand_b = self.ram[self.pc+2]
            # print("IR", IR, "operand A/B", operand_a, operand_b)
            a = format(IR, '08b')[:2]; b = format(IR, '08b')[2:3]; c = format(IR, '08b')[2:][3:4]; d = format(IR, '08b')[2:][4:]
            # print(f"a: {a}, b: {b}, c: {c}, d: {d}")
            number_operands = (IR & 0b11000000) >> 6


            # self.pc += int(a,2) + 1 # Naive implementation
            self.pc += number_operands + 1
            # print("self.pc", self.pc) 


            
            if IR == 0b00000001:
                running = False 
                print("Halted")
            elif IR == 0b10000010: # LDI register immediate
                self.register[int(format(operand_a, '08b')[-3:])] = operand_b
                # print("register", self.register)
            elif IR == 0b01000111: # Print value of register in operand a
                print(f"Value in register {operand_a}: {self.register[operand_a]}")

            








if __name__ == "__main__":
        
    cpu = CPU()
    print(cpu.ram_read(4))
    cpu.ram_write(5,4)
    print(cpu.ram_read(4))
    cpu.run()
    while True:
        x = input("Enter a command: ")
        if x == 'q':
            quit()
        try:
            x
        except:
            print("error")