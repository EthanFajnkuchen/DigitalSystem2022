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
        self.tknzr = Tokenizer
        self.xml_file = open(xml_file_path, "w")

    def set_tokenizer(self, jack_file_path):
        self.tknzr = self.tknzr.Tokenizer(jack_file_path, self.xml_file)

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

    # close the file
    def close(self):
        self.xml_file.close()

    def compile_do(self):
        self.fastforward(2)  # print "do" and the function name or array name imagine "obj_arr[3].callfunc"
        self.compile_subroutineCall()
        self.fastforward()  # print ";"

    def compile_subroutineCall(self, end_term=False):
        import re
        Sub = re.compile(r'^\(|\[|\.$')
        while Sub.match(self.command):
            if self.command == "(":
                self.compile_expression_list()
            elif self.command == ".":
                self.fastforward(2)
            elif self.command == "[":
                self.compile_expression_list(sub_call=False)
        if end_term:
            self.write_labels(start=False, statement="term")

    def compile_expression_list(self, sub_call=True):
        self.fastforward()  # print "("
        if sub_call:
            self.write_labels(statement="expressionList")
            while self.command != ")":
                if self.command == ",":
                    self.fastforward()
                else:
                    self.compile_expression()
            self.write_labels(start=False, statement="expressionList")
        else:
            self.compile_expression()
        self.fastforward()  # print ")"

    import re

    def compile_expression(self, expression=True):
        Integer = re.compile(r'^\d+$')
        String = re.compile(r'^\"[^"]*\"$')
        Keyword = re.compile(r'^true|false|null|this$')
        Identifier = re.compile(r'^[a-zA-Z]+[a-zA-Z_0-9]*$')
        Unary = re.compile(r'^-|~$')
        Op = re.compile(r'^\+|\-|\*|\/|\&|\||<|>|=$')

        if expression:
            self.write_labels(statement="expression")
        self.write_labels(statement="term")

        if Integer.match(self.command):
            current_expression_seg = "integerConstant"
            self.fastforward()
            self.compile_op()
        elif String.match(self.command):
            current_expression_seg = "stringConstant"
            self.fastforward()
            self.compile_op()
        elif Keyword.match(self.command):
            current_expression_seg = "keywordConstant"
            self.fastforward()
            self.compile_op()
        elif Identifier.match(self.command):
            current_expression_seg = "identifier"
            self.fastforward()
            if Op.match(self.command):
                self.compile_op()
            else:
                self.compile_subroutineCall(end_term=True)
        elif self.command == "(":
            current_expression_seg = "("
            self.compile_expression_list(sub_call=False)
            self.compile_op()
        else:
            return None

        if expression:
            self.write_labels(start=False, statement="expression")

    def current_expression_seg(self):
        Integer = re.compile(r'^\d+$')
        String = re.compile(r'^\"[^"]*\"$')
        Keyword = re.compile(r'^true|false|null|this$')
        Identifier = re.compile(r'^[a-zA-Z]+[a-zA-Z_0-9]*$')
        Unary = re.compile(r'^-|~$')
        Op = re.compile(r'^\+|\-|\*|\/|\&|\||<|>|=$')
        if Integer.match(self.command):
            return "integerConstant"
        elif String.match(self.command):
            return "stringConstant"
        elif Keyword.match(self.command):
            return "keywordConstant"
        elif Identifier.match(self.command):
            return "identifier"
        elif Unary.match(self.command):
            # has some logic flaw here: if symbol is "-", the program will always
            # recognize it as a "Unary", but sometimes it can be an Op
            return "unaryOp"
        elif Op.match(self.command):
            return "Op"
        elif self.command == "(":
            return "("
        else:
            return None

    def compile_op(self, write_statement=True, unary=False):
        Unary = re.compile(r'^-|~$')
        Op = re.compile(r'^\+|\-|\*|\/|\&|\||<|>|=$')
        if write_statement:
            self.write_labels(start=False, statement="term")
        if re.match(Op, self.command) or re.match(Unary, self.command):
            self.fastforward()
            self.compile_expression(expression=False)
        if unary:
            self.write_labels(start=False, statement="term")

    def command(self):
        return self.tknzr.current_command

    def write_labels(self, statement, start=True):
        self.xml_file.write(f"<{'' if start else '/'}{statement}>\n")

    def fastforward(self, n=1):
        for i in range(n):
            self.tknzr.write_command()
            self.tknzr.advance()
