import glob
import os
import sys
import CompileEngine


class JackAnalyzer:
    def __init__(self, path):
        self.compileengine = CompileEngine
        if path[-1] == "/":
            path = path[0:-1]
        self.jack_path = os.path.expanduser(path)
        self.single_file = True if path[-5:] == ".jack" else False
        print(self.single_file)

    def compile(self):
        if self.single_file:
            self.compile_one(self.jack_path)
        else:
            self.compile_all()
        self.compileengine.CompileEngine.close()

    def compile_one(self, jack_path):
        xml_path = jack_path.replace(".jack", ".xml")
        self.compileengine = self.compileengine.CompileEngine(xml_path)
        print("Engine Created")
        self.compileengine.set_tokenizer(jack_path)
        print("Tokenizer Created")
        self.compileengine.write()
        self.compileengine.close()

    def compile_all(self):
        print("compiling a folder")
        for file in glob.glob(f"{self.jack_path}/*.jack"):
            print(file)
            self.compile_one(file)


if __name__ == "__main__":
    JackAnalyzer("Square.jack").compile()
