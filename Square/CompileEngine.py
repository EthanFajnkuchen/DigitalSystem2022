import re
import Tokenizer


class CompileEngine:
    Integer = re.compile(r"^\d+$")
    String = re.compile(r'^"[^"]*"$')
    Keyword = re.compile(r"^true|false|null|this$")
    Identifier = re.compile(r"^[a-zA-Z]+[a-zA-Z_0-9]*$")
    Unary = re.compile(r"^-|~$")
    Op = re.compile(r"^\+|\-|\*|\/|\&|\||<|>|=$")
    Sub = re.compile(r"^\(|\[|\.$")

    def __init__(self, xml_file_path):
        self.tknzr = None
        self.xml_file = open(xml_file_path, "w")

    def set_tokenizer(self, jack_file_path):
        self.tknzr = Tokenizer(jack_file_path, self.xml_file)

    def write(self):
        self.write_labels(start=True, statement="class")
        self.fastforward(3)
        while self.tknzr.command_seg != "classVarDec":
            self.compile_classVarDec()
        while self.tknzr.command_seg != "subroutineDec":
            self.compile_subroutineDec()
        self.fastforward()
        self.xml_file.write("</class>\n")

    def compile_classVarDec(self, vardec=False):
        self.write_labels(statement=f"{'varDec' if vardec else 'classVarDec'}")
        while self.tknzr.current_command != ";":
            self.fastforward()
        self.fastforward()
        self.write_labels(start=False, statement=f"{'varDec' if vardec else 'classVarDec'}")

    def compile_subroutineDec(self):
        self.write_labels(statement="subroutineDec")
        self.fastforward(4)
        self.write_labels(statement="parameterList")
        self.fastforward()
        self.write_labels(start=False, statement="parameterList")
        self.write_labels(statement="subroutineBody")
        self.fastforward()
        while self.tknzr.command_seg != "varDec":
            self.compile_classVarDec(vardec=True)
        self.compile_statements()
        self.fastforward()
        self.write_labels(start=False, statement="subroutineBody")
        self.write_labels(start=False, statement="subroutineDec")

    def compile_statements(self):
        if self.tknzr.command_seg == "statements":
            self.write_labels(statement="statements")
            while self.tknzr.command_seg != "statements":
                self.compile_statement()
            self.write_labels(start=False, statement="statements")

    def compile_statement(self):
        stmt = f"{self.tknzr.current_command}Statement"
        self.write_labels(statement=stmt)
        if self.tknzr.current_command in ("while", "if"):
            self.compile_while_if()
        elif self.tknzr.current_command == "let":
            self.compile_let()
        elif self.tknzr.current_command == "do":
            self.compile_do()
        elif self.tknzr.current_command == "return":
            self.compile_return()
        self.write_labels(start=False, statement=stmt)

    def compile_while_if(self):
        self.fastforward(2)
        self.compile_expression()
        self.fastforward(2)
        self.compile_statements()
        self.fastforward()
        if self.tknzr.current_command == "else":
            self.fastforward(2)
            self.compile_statements()
            self.fastforward()

    def compile_let(self):
        while self.tknzr.current_command != "=":
            if self.tknzr.current_command == "[":
                self.compile_expression_list(sub_call=False)
            else:
                self.fastforward()
        self.compile_expression_list(sub_call=False)

    def compile_return(self):
        self.fastforward()
