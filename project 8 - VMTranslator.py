import os
import sys


class Parser:
    """
    reading the file to list of commands with @self.commands
    such that @self.command is the command in the current line and @self.curr is the counter
    """

    def __init__(self, input_file: str):
        self.command = ""
        self.curr = -1
        self.commands = []

        file = open(input_file)
        for line in file:  # insert each line to the list
            line = line.partition("//")[0]
            line = line.strip()
            if line:
                self.commands.append(line)
        file.close()  # closing the file

    def hasMoreLine(self):  # check if there exist more lines in the file
        return (self.curr + 1) < len(self.commands)

    def advance(self):  # moving to the next line of the file
        self.curr += 1
        self.command = self.commands[self.curr]

    def commandType(self):  # returning the desired command
        command = self.command.split(" ")[0]
        if command == "pop":
            return "C_POP"

        if command == "push":
            return "C_PUSH"

        if command == "add" or command == "sub" or command == "neg" or command == "eq" or command == "gt" or command == "lt" or command == "and" or command == "or" or command == "not":
            return "C_ARITHMETIC"

        if "label" == command:
            return "C_LABEL"

        if "goto" == command:
            return "C_GOTO"

        if "if-goto" == command:
            return "C_IF-GOTO"

        if "call" == command:
            return "C_CALL"

        if "function" == command:
            return "C_FUNCTION"

        if "return" == command:
            return "C_RETURN"

    def args1(self):  # returning the first args by the command type
        if self.commandType() == "C_ARITHMETIC" or self.commandType() == "C_RETURN":
            return self.command.split(" ")[0]
        else:
            return self.command.split(" ")[1]

    def args2(self):  # returning the second args by the command type
        if ("C_PUSH" or "C_POP" or "C_CALL" or "C_FUNCTION") == self.commandType():
            return self.command.split(" ")[2]


class CodeWriter:
    """
    opening the given file and by the @self.fileWriter
    and counting the number of labels by the @self.label
    """

    def __init__(self, file: str):
        self.fileWriter = open(file, "w")
        self.label = 0  # counting the number of labels
        self.function_count = 0  # counting the number of function
        self.call_count = 0  # counting the number of calls

    '''init the function'''
    def write_init(self): 
        self.write("@256\nD=A\n@SP\nM=D\n@Sys.init\n0;JMP")
        self.function_count += 1

    # writing to the file the arithmetic commands
    def writeArithmetic(self, command: str):
        # build a dictionary of the commands
        CommandDictionary = {
            "add": "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=D+M\n@SP\nM=M+1\n",
            "sub": "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nM=M-D\n@SP\nM=M+1\n",
            "neg": "@SP\nA=M-1\nM=-M\n",
            "not": "@SP\nA=M-1\nM=!M\n",
            "or": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D|M\n",
            "and": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D&M\n",
            "eq": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@eqTrue" + str(self.label) + "\nD;JEQ\n@SP\nA=M-1\nM=0\n("
                                                                                           "eqTrue" + str(
                self.label) + ")\n",
            "gt": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@gtTrue" + str(self.label) + "\nD;JGT\n@SP\nA=M-1\nM=0\n("
                                                                                           "gtTrue" + str(
                self.label) + ")\n ",
            "lt": "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nD=M-D\nM=-1\n@ltTrue" + str(self.label) + "\nD;JLT\n@SP\nA=M-1\nM=0\n("
                                                                                           "ltTrue" + str(
                self.label) + ")\n "
        }
        if CommandDictionary[command] is not None:
            self.fileWriter.write(CommandDictionary[command])  # get the value from the dictionary to the file
            if command == "eq" or "lt" or "gt":
                self.label += 1  # increase the label counter by 1

    def WritePushPop(self, command: str, segment: str, index: str):
        # build a dictionary of the commands
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
            "local C_PUSH": "@" + index + "\nD=A\n@LCL\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "local C_POP": "@" + index + "\nD=A\n@LCL\nD=M+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
            "temp C_PUSH": "@" + index + "\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "temp C_POP": "@" + index + "\nD=A\n@5\nD=A+D\n@R13\nM=D\n@SP\nAM=M-1\nD=M\n@R13\nA=M\nM=D\n",
        }
        com = segment + " " + command  # making the key for the dictionary
        if SegmentDictionary[com] is not None:
            self.fileWriter.write(SegmentDictionary[com])  # getting the value from the dictionary to the file

    def writeLabel(self, label: str):
        self.fileWriter.write("(" + label + ")")

    def writeGoto(self, label: str):
        self.fileWriter.write("@" + label + "\n0;JMP\n")

    def writeIf(self, label: str):
        self.fileWriter.write("@SP\nAM=M-1\nD=M\n@" + label + "\nD;JNE\n")

    def writeCall(self, functionName: str, nArgs: int):
        RETURN_UNIQUE = functionName + "RETURN" + str(self.call_count)
        self.fileWriter.write("@" + RETURN_UNIQUE + "\nD=A\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\n@ARG\n"
                                                    "@THIS\n@THAT\n@SP\nD=M\n@LCL\nM=D\n@"
                              + str(nArgs + 5) + "D=A\n@SP\nD=M-D\n@ARG\nM=D\n@" + functionName + "\n0;JMP\n")
        # Return address
        self.fileWriter.write(f'({RETURN_UNIQUE})', code=False)

    def writeFunction(self, functionName: str, nVars: int):
        self.fileWriter.write(
            "(" + functionName + ")\n@" + str(
                nVars) + "\nD=A\n@i\nM=D\n(LOOP)\n@i\nD=M\n@END\nD;JEQ\n@SP\nAM=M+1\nA=A-1"
                         "\nM=0\n@i\nM=M-1\n@LOOP\n0;JMP\n(END)\n"
        )

    def writeReturn(self):
        address_list = ['@THAT', '@THIS', '@ARG', '@LCL']
        self.fileWriter.write(
            "@LCL\nD=M\n@R13\nM=D\n@R13\nD=M\n@5\nD=D-A\nA=D\nD=M\n@R14\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M"
            "\nM=D\n@ARG\nD=M\n@SP\nM=D+1")
        counter = 1
        for item in address_list:
            self.fileWriter.write("@R13\nD=M\n@" + str(counter) + "\nD=D-A\nA=D\nD=M\n" + item + "M=D\n")
            counter += 1
        self.fileWriter.write("@R14\nA=M\n0;JMP")

    def close(self):
        """Closes the output file."""
        self.fileWriter.close()


def VMTranslator():
    input_file = sys.argv[1]  # reading a file
    output_file = input_file.replace(".vm", ".asm")  # switching to asm file
    parser = Parser(input_file)  # build a parser
    code_writer = CodeWriter(output_file)
    # making the code writer to the output file
    while parser.hasMoreLine():
        parser.advance()
        comm_type = parser.commandType()
        if comm_type == "C_ARITHMETIC":  # its arithmetic
            code_writer.writeArithmetic(parser.args1())

        elif comm_type == "C_POP" or comm_type == "C_PUSH":  # it is push or pop functions
            arg1 = parser.args1()
            arg2 = parser.args2()
            code_writer.WritePushPop(comm_type, arg1, arg2)

        elif comm_type == "C_LABEL":
            code_writer.writeLabel(parser.args1())

        elif comm_type == "C_GOTO":
            code_writer.writeGoto(parser.args1())

        elif comm_type == "C_IF-GOTO":
            code_writer.writeIf(parser.args1())

        elif comm_type == "C_FUNCTION":
            code_writer.writeFunction(parser.args1(), parser.args2())

        elif comm_type == "C_CALL":
            code_writer.writeCall(parser.args1(), parser.args2())

        elif comm_type == "C_RETURN":
            code_writer.writeReturn()

    code_writer.close()  # close the file


if __name__ == "__main__":
    VMTranslator()
