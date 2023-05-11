import os
import sys


class Code:

    def __init__(self):
        self.destinationTable = {
            "": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }

        self.jumpTable = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

        self.compTable = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "M": "1110000",
            "!D": "0001101",
            "!A": "0110001",
            "!M": "1110001",
            "-D": "0001111",
            "-A": "0110011",
            "-M": "1110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "M+1": "1110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "M-1": "1110010",
            "D+A": "0000010",
            "D+M": "1000010",
            "D-A": "0010011",
            "D-M": "1010011",
            "A-D": "0000111",
            "M-D": "1000111",
            "D&A": "0000000",
            "D&M": "1000000",
            "D|A": "0010101",
            "D|M": "1010101"
        }

    def dest(self, pattern):
        return self.destinationTable[pattern]

    def jump(self, pattern):
        return self.jumpTable[pattern]

    def comp(self, pattern):
        return self.compTable[pattern]


class Parser:

    def __init__(self, file_name):
        self.command = ""
        self.curr = -1
        self.commands = []

        file = open(file_name)
        for line in file:
            line = line.partition("//")[0]
            line = line.strip()
            line = line.replace(" ", "")
            if line:
                self.commands.append(line)
        file.close()

    # Check if we finished to parse the file
    def hasMoreLines(self):
        return (self.curr + 1) < len(self.commands)

    # Go to the next instruction and make it current
    def advance(self):
        self.curr += 1
        self.command = self.commands[self.curr]

    # Determine the instruction type and returns it
    def instructionType(self):
        if self.command[0] == "@":
            return "A"
        elif self.command[0] == "(":
            return "L"
        else:
            return "C"

    # Return the instruction symbol
    def symbol(self):
        if self.instructionType() == "A":
            return self.command[1:]
        if self.instructionType() == "L":
            return self.command[1:-1]

    # Return the dest field
    def dest(self):
        if self.instructionType() == "C":
            if "=" in self.command:
                return self.command.partition("=")[0]
        return ""

    # Return the comp field
    def comp(self):
        if self.instructionType() == "C":
            tmp = self.command
            if "=" in tmp:
                tmp = tmp.partition("=")[2]
            return tmp.partition(";")[0]
        return ""

    # Return the jump field
    def jump(self):
        if self.instructionType() == "C":
            tmp = self.command
            if "=" in tmp:
                tmp = tmp.partition("=")[2]
            return tmp.partition(";")[2]
        return ""


class SymbolTable:

    def __init__(self):
        self.table = {
            "R0": 0,
            "R1": 1,
            "R2": 2,
            "R3": 3,
            "R4": 4,
            "R5": 5,
            "R6": 6,
            "R7": 7,
            "R8": 8,
            "R9": 9,
            "R10": 10,
            "R11": 11,
            "R12": 12,
            "R13": 13,
            "R14": 14,
            "R15": 15,
            "SCREEN": 16384,
            "KBD": 24576
        }

    def addEntry(self, symbol, address):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def getAddress(self, symbol):
        return self.table[symbol]


def HackAssembler():
    #Create the parser related to the file
    file = sys.argv[1]
    parser = Parser(file)

    symbols = SymbolTable()

    counter = 0
    while parser.hasMoreLines():
        parser.advance()
        if parser.instructionType() == "L":
            symbols.addEntry(parser.symbol(), counter)
        else:
            counter += 1

    parser.command = ""
    parser.curr = -1

    translator = Code() # Create the generator of binary code object

    outputName = file.replace(".asm", ".hack") #Change the type of the file output to hack
    file = open(outputName, "w")

    addressAvailable = 16
    while parser.hasMoreLines():
        parser.advance()

        if parser.instructionType() == "A":
            num = 0
            symbol = parser.symbol()
            isDecimal = False
            isLabelOrExist = False

            if symbols.contains(symbol):
                num = symbols.getAddress(symbol)
                isLabelOrExist = True


            if symbol.isdecimal():
                num = int(symbol)
                isDecimal = True

            if isDecimal == False and isLabelOrExist == False:
                num = addressAvailable
                symbols.addEntry(symbol, num)
                addressAvailable += 1

            file.write(format(num, "016b"))  # Complete to 16 bits
            file.write("\n")

        if parser.instructionType() == "C":
            comp = translator.comp(parser.comp())
            dest = translator.dest(parser.dest())
            jump = translator.jump(parser.jump())
            file.write("111" + comp + dest + jump)
            file.write("\n")

    file.close()


if __name__ == "__main__":
    HackAssembler()