import os.path
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
        if "C_PUSH" or "C_POP" or "C_CALL" or "C_FUNCTION" == self.commandType():
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
        self.fileName = ""
        self.functionName = "OS"

    '''init the function'''

    def writeInit(self):
        self.fileWriter.write("@256\nD=A\n@SP\nM=D\n")
        self.writeFunction("OS", 0)
        self.writeCall("Sys.init", 0)
        self.function_count += 1

    def setFileName(self, file_name):
        self.fileName = file_name

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
        if SegmentDictionary.get(com) is not None:
            self.fileWriter.write(SegmentDictionary.get(com))  # getting the value from the dictionary to the file

    def writeLabel(self, label: str):
        self.fileWriter.write("(" + self.functionName + "$" + label + ")\n")

    def writeGoto(self, label: str):
        self.fileWriter.write("@" + self.functionName + "$" + label + "\n0;JMP\n")

    def writeIf(self, label: str):
        self.fileWriter.write("@SP\nAM=M-1\nD=M\n" + "@" + self.functionName + "$" + label + "\nD;JNE\n")

    def writeCall(self, functionName: str, nArgs: int):
        self.fileWriter.write(
            "@" + self.functionName + "$ret." + str(self.label) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        for i in ["LCL", "ARG", "THIS", "THAT"]:
            self.fileWriter.write("@" + i + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.fileWriter.write("@SP\nD=M\n@5\nD=D-A\n" + "@" + str(
            nArgs) + "\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n" + "@" + functionName + "\n0;JMP\n" + 
                              "(" + self.functionName + "$ret." + str(self.label) + ")\n")
        self.label += 1

    def writeFunction(self, functionName: str, nVars: int):
        self.functionName = functionName
        self.fileWriter.write("(" + functionName + ")\n")
        for i in range(int(nVars)):
            self.WritePushPop("C_PUSH", "constant", '0')

    def writeReturn(self):
        address_list = ['@THAT', '@THIS', '@ARG', '@LCL']
        self.fileWriter.write(
            "@LCL\nD=M\n@R13\nM=D\n@5\nA=D-A\nD=M\n@R14\nM=D\n@SP\nAM=M-a\nD=M\n@ARG\nD=M+1\n@SP\nM=D\n")
        for item in address_list:
            self.fileWriter.write("@R13\nAM=M-1\nD=M\n" + "@" + item + "\nM=D\n")
        self.fileWriter.write("@R14\nA=M\n0;JMP\n")

    def close(self):
        """Closes the output file."""
        self.fileWriter.close()


def VMTranslator():
    path_given = sys.argv[1]  # reading a file
    list_of_input = []
    isFile = False
    bootstrap = False
    if os.path.isfile(path_given) and path_given.endswith(".vm"):
        list_of_input.append(path_given)
        output_file = path_given.replace(".vm", ".asm")
        isFile = True

    if os.path.isdir(path_given):
        if path_given.endswith("/"):
            path_given = path_given[:-1]
        list_of_files_in_dir = os.listdir(path_given)
        for file in list_of_files_in_dir:
            if file.endswith(".vm"):
                list_of_input.append(path_given + "/" + file)
            if file == "Sys.vm":
                bootstrap = True

        output_file = path_given + "/" + os.path.basename(os.path.normpath(path_given)) + ".asm"

    for input_file in list_of_input:
        code_writer = CodeWriter(output_file)
        code_writer.setFileName(output_file)
        if not isFile and bootstrap:
            code_writer.writeInit()
        parser = Parser(input_file)
        # making the code writer to the output file
        while parser.hasMoreLine():
            parser.advance()
            comm_type = parser.commandType()
            if comm_type == "C_ARITHMETIC":  # its arithmetic
                code_writer.writeArithmetic(parser.args1())

            elif comm_type == "C_POP" or comm_type == "C_PUSH":  # it is push or pop functions
                arg1 = parser.args1()
                arg2 = parser.args2()
                code_writer.WritePushPop(comm_type, arg1, str(arg2))

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


if __name__ == "_main_":
    VMTranslator()
