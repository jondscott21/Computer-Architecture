"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
MULT = 0b10100010
HLT = 0b00000001
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #  Random access memory -- ram
        self.ram = [0] * 256
        #  Process register -- reg
        self.reg = [0] * 8
        # Process counter -- pc
        self.pc = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MULT] = self.handle_MULT
        self.branchtable[HLT] = self.handle_HLT
        self.running = False

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    # print(line)
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue
                    instruction = int(num,2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")

        # # For now, we've just hardcoded a program:
        # address = 0
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
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

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    
    def handle_LDI(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc += 3
    def handle_PRN(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2
    def handle_MULT(self):
        self.alu("MULT", self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
        self.pc += 3
    def handle_HLT(self):
        self.running = False
    def run(self):
        """Run the CPU."""
        self.running = True    
        while self.running:
            IR = self.ram[self.pc]
            self.branchtable[IR]()

