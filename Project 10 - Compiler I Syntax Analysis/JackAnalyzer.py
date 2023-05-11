import re
from os import listdir
from os.path import isfile, isdir
from CompilationEngine import CompilationEngine
import sys


jack_input = re.compile(".*\.jack$")


def get_files(args):
    """
    :param args: the arguments given to the program.
    :return: the list of paths to .jack files
    """
    list_of_files_path = []
    if len(args) == 2: #If the number of arguments input is 2
        if isfile(args[1]) and jack_input.match(args[1]): #If the path is a file and it's a jack file
            list_of_files_path.append(args[1]) #add it to the list of input files
        elif isdir(args[1]): #if the path is a dir
            for file in listdir(args[1]): #go over each file in the dir
                if jack_input.match(file): #if the file is a jack file
                    list_of_files_path.append(args[1] + "/" + file) #add it to the list of file
        return list_of_files_path
    else:
        print("The path given is unvalid")
        exit()


def file_output_path(file_path):
    output_path = re.sub(".jack", ".xml", file_path) #replace the .jack by .xml
    return output_path


if __name__ == "__main__":
    list_of_files_path = get_files(sys.argv)
    for file_path in list_of_files_path:
        to_compile = CompilationEngine(file_path, file_output_path(file_path))
        to_compile.compileClass()
