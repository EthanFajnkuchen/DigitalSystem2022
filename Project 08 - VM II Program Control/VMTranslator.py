import os.path
import sys


class Parser:
    """
    The Parser class.
    We will use it to read VM commands from the input file.
    """


    """
    Constructor of the Parser object.
    We initialize 3 fields : - The actual command
                             - The
                             - A list of all VM commands contains in the file
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

    """
    We check if there exist more lines to parse in the file.
    The value return is True or False.
    """
    def hasMoreLine(self):
        return (self.curr + 1) < len(self.commands)

    """
    We move to the next command in the file.
    Actually, we just move the pointer to the element in the list and change the command field by the new command 
    pointed by the curr field in the list.
    """
    def advance(self):
        self.curr += 1
        self.command = self.commands[self.curr]

    """
    We return the command type of the VM command.
    There exists 9 types of commands :
                                            - POP
                                            - PUSH
                                            - ARITHMETIC
                                            - LABEL
                                            - GOTO
                                            - IF GOTO
                                            - CALL
                                            - FUNCTION
                                            - RETURN
    """
    def commandType(self):
        command = self.command.split(" ")[0]
        if command == "pop":
            return "C_POP"

        if command == "push":
            return "C_PUSH"

        if command == "add" or command == "sub" or command == "neg" or command == "eq" or command == "gt" or \
                command == "lt" or command == "and" or command == "or" or command == "not":
            return "C_ARITHMETIC"

        if command == "label":
            return "C_LABEL"

        if command == "goto":
            return "C_GOTO"

        if command == "if-goto":
            return "C_IF-GOTO"

        if command == "call":
            return "C_CALL"

        if command == "function":
            return "C_FUNCTION"

        if "return" == command:
            return "C_RETURN"

    """
    Return the first argument of the command.
    We separate in two cases, when the command type is ARITHMETIC or RETURN and the when the command type is one of the seven others.
    """
    def args1(self):
        if self.commandType() == "C_ARITHMETIC" or self.commandType() == "C_RETURN":
            return self.command.split(" ")[0]
        else:
            return self.command.split(" ")[1]

    """
    Return the second argument of the command.
    This function is used only for Push,Pop,Call or Function command.
    """
    def args2(self):
        if "C_PUSH" or "C_POP" or "C_CALL" or "C_FUNCTION" == self.commandType():
            return self.command.split(" ")[2]


class CodeWriter:
    """
    The CodeWriter class.
    We will use the CodeWriter object to translate the VM commands in ASM language.
    """

    """
    Constructor of the CodeWriter object.
    We initialize 4 fields :
                            - fileWriter   : this field is our writer, we will use it to write into the output file.
                            - label        : this field is our label counter. 
                            - fileName     : this field keep the name of the inputFile into the CodeWriter object, it 
                                              will be useful when parsing multiple VM files in a directory.
                            - functionName : this field keep the name of the function that we are translating.
    """
    def __init__(self, file: str):
        self.fileWriter = open(file, "w")
        self.label = 0  # counting the number of labels
        self.fileName = ""
        self.functionName = ""

    """
    This function write the boostrap code into the output file.
    It should be call when we get a Directory as an input and the given Directory includes the Sys.vm file.
    """
    def writeInnit(self):
        self.fileWriter.write("@256\nD=A\n@SP\nM=D\n")
        self.functionName = "Sys.init"
        self.writeCall("Sys.init",0)

    """
    We keep the input file name into our CodeWriter object.
    We need this setter to indicate to the CodeWriter when a translation of a new VM file has started.
    """
    def setFileName(self,file_name):
        self.fileName = file_name

    """
    Writes to the output file the assembly code that implements the given arithmetic command.
    On this purpose, we build a dictionary of all the commands and return for each arithmetic command the value 
    associated to the key. Here the key is the actual VM command.
    """
    def writeArithmetic(self, command: str):
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
            self.fileWriter.write(CommandDictionary[command])
            if command == "eq" or "lt" or "gt":
                self.label += 1  # increase the label counter by 1

    """
    Writes to the output file the assembly code that implements the given push or pop command.
    On this purpose, we build a dictionary of all the commands and return for each pop/push command the value 
    associated to the key. Here the key is the a composition of the command associated to the given segment.
    """
    def WritePushPop(self, command: str, segment: str, index: str):
        SegmentDictionary = {
            "constant C_PUSH": "@" + index + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "static C_PUSH": "@" + self.fileName + "." + index + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n",
            "static C_POP": "@SP\nAM=M-1\nD=M\n@" + self.fileName + "." + index + "\nM=D\n",
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

    """
    Write assembly code into the output file that affect the label command.
    """
    def writeLabel(self, label: str):
        self.fileWriter.write("(" + self.functionName + "$" + label + ")\n")

    """
    Write assembly code into the output file that affect the goto command.
    """
    def writeGoto(self, label: str):
        self.fileWriter.write("@" + self.functionName + "$" + label + "\n0;JMP\n")

    """
    Write assembly code into the output file that affect the if-goto command.
    """
    def writeIf(self, label: str):
        self.fileWriter.write("@SP\nAM=M-1\nD=M\n" + "@" + self.functionName + "$" + label + "\nD;JNE\n")

    """
    Write assembly code into the output file that affect the call command.
    """

    def writeCall(self, functionName: str, nArgs: int):
        self.fileWriter.write("@" + self.functionName + "$ret." + str(self.label) +"\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        for i in ["LCL","ARG","THIS","THAT"]:
            self.fileWriter.write("@"+i+"\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        self.fileWriter.write("@SP\nD=M\n@5\nD=D-A\n" + "@" + str(nArgs) + "\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n"
                              + "@" + functionName + "\n0;JMP\n" + "(" + self.functionName + "$ret."
                              + str(self.label) +")\n")

        self.label += 1

    """
    Write assembly code into the output file that affect the function command.
    """
    def writeFunction(self, functionName: str, nVars: int):
        self.functionName = functionName
        self.fileWriter.write("(" + self.functionName + ")\n")
        for i in range(int(nVars)):
            self.WritePushPop("C_PUSH","constant",'0')

    """
    Write assembly code into the output file that affect the return command.
    """
    def writeReturn(self):
        self.fileWriter.write("@LCL\nD=M\n@R11\nM=D\n@5\nA=D-A\nD=M\n@R12\nM=D\n@ARG\nD=M\n@0\nD=D+A\n@R13\nM=D\n@SP\n"
                              "AM=M-1\nD=M\n@R13\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n@R11\nD=M-1\nAM=D\nD=M\n@THAT\nM=D\n"
                              "@R11\nD=M-1\nAM=D\nD=M\n@THIS\nM=D\n@R11\nD=M-1\nAM=D\nD=M\n@ARG\nM=D\n@R11\nD=M-1\n"
                              "AM=D\nD=M\n@LCL\nM=D\n@R12\nA=M\n0;JMP\n")

    """
    We close the writer of the CodeWriter object when the translation of all the VM commands in each file provided
    is done.
    """
    def close(self):
        self.fileWriter.close()


    """
    Our main function that use the Parser and CodeWriter classes to actually translate the VM files.
    """
def VMTranslator():
    path_given = sys.argv[1]
    list_of_input = []
    isFile = False
    bootstrap = False

    # We first check if the path given is a file.
    if os.path.isfile(path_given) and path_given.endswith(".vm"):
        list_of_input.append(path_given)
        output_file = path_given.replace(".vm", ".asm") #Create an output file where the name is fileName.asm.
        isFile = True

    # We now check if the path given is a directory.
    if os.path.isdir(path_given):
        if path_given.endswith("/"):
            path_given = path_given[:-1]
        list_of_files_in_dir = os.listdir(path_given)
        for file in list_of_files_in_dir:
            if file.endswith(".vm"):
                list_of_input.append(path_given + "/" + file) # We add every VM files to a list to keep them.
            if file == "Sys.vm":
                bootstrap = True

        #We create the output file in the case a directory is given, here the name is DirName.asm
        output_file = path_given + "/" + os.path.basename(os.path.normpath(path_given)) + ".asm"

    code_writer = CodeWriter(output_file) #We create the code writer.
    for input_file in list_of_input:
        code_writer.setFileName(os.path.basename(input_file).split('/')[-1]) #We set the file name to the input file that we parse.
        if isFile == False and bootstrap == True:
            code_writer.writeInnit()
        parser = Parser(input_file) #We create the parser to read the input file and begin the translation.

        while parser.hasMoreLine():
            parser.advance()
            comm_type = parser.commandType()

            if comm_type == "C_ARITHMETIC":
                code_writer.writeArithmetic(parser.args1())

            elif comm_type == "C_POP" or comm_type == "C_PUSH":
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

    code_writer.close()  # We close the file when the translation is done.


if __name__ == "__main__":
    VMTranslator()