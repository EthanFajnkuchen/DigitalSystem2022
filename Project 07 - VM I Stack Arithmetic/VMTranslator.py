import sys


class Parser:
    """
    reading the file to list of commands with @self.commands
    such that @self.command is the command in the current line and @self.curr is the counter
    """

    def __init__(self, input_file):
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

    def args1(self):  # returning the first args by the command type
        if self.commandType() == "C_ARITHMETIC":
            return self.command.split(" ")[0]
        else:
            return self.command.split(" ")[1]

    def args2(self):  # returning the second args by the command type
        if self.commandType() == "C_PUSH" or self.commandType() == "C_POP":
            return self.command.split(" ")[2]


class CodeWriter:
    """
    opening the given file and by the @self.fileWriter
    and counting the number of labels by the @self.label
    """

    def __init__(self, file):
        self.fileWriter = open(file, "w")
        self.label = 0  # counting the number of labels

    # writing to the file the arithmetic commands
    def writeArithmetic(self, command):
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

    def WritePushPop(self, command, segment, index):
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

        if comm_type == "C_POP" or comm_type == "C_PUSH":  # it is push or pop functions
            arg1 = parser.args1()
            arg2 = parser.args2()
            code_writer.WritePushPop(comm_type, arg1, arg2)

    code_writer.close()  # close the file


if __name__ == "__main__":
    VMTranslator()