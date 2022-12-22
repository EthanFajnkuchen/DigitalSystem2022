import sys
import os

class Parser :

    def __init__(self,input_file):
        self.command = ""
        self.curr = -1
        self.commands = []

        file = open(input_file)
        for line in file:
            line = line.partition("//")[0]
            line = line.strip()
            #line = line.replace(" ", "")
            if line:
                self.commands.append(line)
        file.close()

    def hasMoreLine(self) :
        return (self.curr + 1) < len(self.commands)

    def advance(self):
        self.curr += 1
        self.command = self.commands[self.curr]

    def commandType(self):
        command = self.command.split(" ")[0]
        if command == "pop":
            return "C_POP"

        if command == "push":
            return "C_PUSH"

        if command == "add" or command == "sub" or command == "neg" or command == "eq" or command == "gt" or command == "lt" or command == "and" or command == "or" or command == "not":
            return "C_ARITHMETIC"

    def args1(self):
        if self.commandType() == "C_ARITHMETIC":
            return self.command.split(" ")[0]
        else :
            return self.command.split(" ")[1]

    def args2(self):
        if self.commandType() == "C_PUSH" or self.commandType() == "C_POP" :
            return self.command.split(" ")[2]

class CodeWriter :

    def __init__(self,file):
        self.fileWriter = open(file,"w")
        self.label = 0
        self.dict_of_symbols = {"add": "M=D+M",
                                "sub": "M=M-D",
                                "and": "M=D&M",
                                "or" : "M=D|M",
                                "neg": "M=-M" ,
                                "not": "M=!M" ,
                                "eq" : "D;JEQ",
                                "gt" : "D;JGT",
                                "lt" : "D;JLT",
                                }

    def writeArithmetic(self, command):
        CommandDictionary = {
            "add": "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D+M\n@SP\nM=M+1\n",
            "sub": "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M-D\n@SP\nM=M+1\n",
            "neg": "@SP\nA=M-1\nM=-M\n",
            "not": "@SP\nA=M-1\nM=!M\n",
            "or": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D|M\n",
            "and": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D&M\n",
            "eq": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@eqTrue" + str(self.label) + "\nD;JEQ\n@SP\nA=M-1\nM=0\n("
                                                                                      "eqTrue" + str(self.label)+ ")\n",
            "gt": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@gtTrue" + str(self.label) + "\nD;JGT\n@SP\nA=M-1\nM=0\n("
                                                                                      "gtTrue" + str(self.label) + ")\n ",
            "lt": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@ltTrue" + str(self.label) + "\nD;JLT\n@SP\nA=M-1\nM=0\n("
                                                                                      "ltTrue" + str(self.label)+ ")\n "
        }
        if CommandDictionary[command] is not None:
            self.fileWriter.write(CommandDictionary[command])
            if command == "eq" or "lt" or "gt":
                self.label += 1

    def WritePushPop(self, command, segment, index):
        SegmentDictionary = {
            "constant C_PUSH": "@" + index + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "static C_PUSH": "@" + index + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "static C_POP": "@SP\nAM=M-1\nD=M\n@" + index + "\nM=D\n",
            "pointer C_PUSH": "@" + index + "\nD=A\n@3\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "pointer C_POP": "@" + index + "\nD=A\n@3\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "this C_PUSH": "@" + index + "\nD=A\n@THIS\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "this C_POP": "@" + index + "\nD=A\n@THIS\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "that C_PUSH": "@" + index + "\nD=A\n@THAT\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "that C_POP": "@" + index + "\nD=A\n@THAT\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "argument C_PUSH": "@" + index + "\nD=A\n@ARG\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "argument C_POP": "@" + index + "\nD=A\n@ARG\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "local C_PUSH": "@" + index + "\nD=A\n@LCL\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "local C_POP": "@" + index + "\nD=A\n@LCL\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "temp C_PUSH": "@" + index + "\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "temp C_POP": "@" + index + "\nD=A\n@5\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
        }
        com = segment + " " + command
        if SegmentDictionary[com] is not None:
            self.fileWriter.write(SegmentDictionary[com])

    def close(self):
        """Closes the output file."""
        self.fileWriter.close()


def VMTranslator() :

    input_file = sys.argv[1]
    output_file = input_file.replace(".vm",".asm")

    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)

    while parser.hasMoreLine() :
        parser.advance()
        comm_type = parser.commandType()
        if comm_type == "C_ARITHMETIC" :
            code_writer.writeArithmetic(parser.args1())

        if comm_type == "C_POP" or comm_type == "C_PUSH" :
            arg1 = parser.args1()
            arg2 = parser.args2()
            code_writer.WritePushPop(comm_type,arg1,arg2)

    code_writer.close()

if __name__ == "__main__" :
    VMTranslator()