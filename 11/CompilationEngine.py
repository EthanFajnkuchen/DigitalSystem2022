from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable

OPERATIONS = {'+': 'add',
              '-': 'sub',
              '*': 'call Math.multiply 2',
              '/': 'call Math.divide 2',
              '&': 'and',
              '|': 'or',
              '<': 'lt',
              '>': 'gt',
              '=': 'eq'
              }


class CompilationEngine:
    """
    The CompilationEngine class reads in a file with the Jack programming language
    and compiles it into XML.
    """

    def __init__(self, input_file_name, output_file_name):
        """
        Initializes the CompilationEngine with an input file name, an output file name,
        and sets the indent count to 0.
        """
        self.indent_count = 0
        self.tokenizer = JackTokenizer(input_file_name)
        self.file_output = open(output_file_name, "w+")
        self.vm_writer = VMWriter(output_file_name)

    def advance(self):
        """
        Advances the tokenizer to the next token.
        """
        self.tokenizer.advance()

    def TokenType(self):
        """
        Returns the type of the current token.
        """
        return self.tokenizer.tokenType()

    def KEYWORD(self):
        """
        Returns the keyword type.
        """
        return self.tokenizer.KEYWORD

    def keyword(self):
        """
        Returns the keyword of the current token.
        """
        return self.tokenizer.keyWord()

    def IDENTIFIER(self):
        """
        Returns the identifier type.
        """
        return self.tokenizer.IDENTIFIER

    def identifier(self):
        """
        Returns the identifier of the current token.
        """
        return self.tokenizer.identifier()

    def indentation(self):
        """
        Returns the current indentation level as a string.
        """
        return "  " * self.indent_count

    def SYMBOL(self):
        """
        Returns the symbol type.
        """
        return self.tokenizer.SYMBOL

    def symbol(self):
        """
        Returns the symbol of the current token.
        """
        return self.tokenizer.symbol()

    def INT_CONST(self):
        """
        Returns the integer constant type.
        """
        return self.tokenizer.INT_CONST

    def STRING_CONST(self):
        """
        Returns the string constant type.
        """
        return self.tokenizer.STRING_CONST

    def current_token(self):
        """
        Return the current token
        """
        return self.tokenizer.currentToken

    def compileClass(self):
        """
        Compiles a complete class.
        """
        if self.tokenizer.hasMoreTokens():
            self.indent_count += 1
            self.advance()
            self.file_output.write("<class>\n")
            self.keyword_writer()
            name = self.tokenizer.advance().value
            jack_class = SymbolTable()
            self.identifier_writer()
            self.advance()
            self.symbol_writer()
            self.advance()
            while self.keyword() in ["static", "field"]:
                self.compileClassVarDec()
            while self.keyword() in ["constructor", "function", "method"]:
                self.compileSubroutine()
            self.symbol_writer()
            self.file_output.write("</class>\n")
            self.file_output.close()
            self.indent_count -= 1

    def compileClassVarDec(self):
        """
        Compiles a static variable declaration or a field declaration.
        """
        self.file_output.write(self.indentation() + "<classVarDec>\n")
        self.indent_count += 1
        self.keyword_writer()
        self.advance()
        self.compile_type_variable()
        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</classVarDec>\n")

    def compileSubroutine(self):
        """
        Compiles a complete method, function, or constructor.
        """

        self.file_output.write(self.indentation() + "<subroutineDec>\n")
        self.indent_count += 1
        self.keyword_writer()
        self.advance()
        if self.TokenType() == self.KEYWORD():
            self.keyword_writer()
        elif self.TokenType() == self.IDENTIFIER():
            self.identifier_writer()
        self.advance()
        self.identifier_writer()
        self.advance()
        self.symbol_writer()
        self.advance()
        self.compileParameterList()
        self.symbol_writer()
        self.advance()

        # compile subroutineBody:
        self.file_output.write(self.indentation() + "<subroutineBody>\n")
        self.indent_count += 1
        self.symbol_writer()
        self.advance()
        while self.keyword() == "var":
            self.compileVarDec()
        self.compileStatements()
        self.symbol_writer()
        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</subroutineBody>\n")
        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</subroutineDec>\n")
        self.advance()

    def compileParameterList(self):
        """
        Compiles a (possibly empty) parameter list.
        """
        self.file_output.write(self.indentation() + "<parameterList>\n")
        self.indent_count += 1
        while self.TokenType() != self.SYMBOL():
            if self.TokenType() == self.KEYWORD():
                self.keyword_writer()
            elif self.TokenType() == self.IDENTIFIER():
                self.identifier_writer()
            self.advance()
            self.identifier_writer()
            self.advance()
            if self.symbol() == ",":
                self.symbol_writer()
                self.advance()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</parameterList>\n")

    def compileVarDec(self):
        """
        Compiles a variable declaration.
        """
        self.file_output.write(self.indentation() + "<varDec>\n")
        self.indent_count += 1

        self.keyword_writer()
        self.advance()
        self.compile_type_variable()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</varDec>\n")

    def compileStatements(self):
        """
        Compiles a sequence of statements, not including the enclosing "{}".
        """
        self.file_output.write(self.indentation() + "<statements>\n")
        self.indent_count += 1
        while self.TokenType() == self.KEYWORD():
            if self.keyword() == "let":
                self.compileLet()
            elif self.keyword() == "if":
                self.compileIf()
            elif self.keyword() == "while":
                self.compileWhile()
            elif self.keyword() == "do":
                self.compileDo()
            elif self.keyword() == "return":
                self.compileReturn()
        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</statements>\n")

    def compileDo(self):
        """compile the Do statement"""
        self.file_output.write(self.indentation() + "<doStatement>\n")
        self.indent_count += 1
        self.keyword_writer()

        self.advance()
        # subroutineCall
        self.identifier_writer()
        self.advance()
        if self.symbol() == ".":
            self.symbol_writer()
            self.advance()
            self.identifier_writer()
            self.advance()

        self.symbol_writer()

        self.advance()
        self.compileExpressionList()

        self.symbol_writer()

        self.advance()
        self.symbol_writer()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</doStatement>\n")
        self.advance()

    def compileLet(self):
        """compile the Let statement"""
        self.file_output.write(self.indentation() + "<letStatement>\n")
        self.indent_count += 1
        self.keyword_writer()

        self.advance()
        self.identifier_writer()

        self.advance()
        if self.symbol() == "[":
            self.symbol_writer()
            self.advance()
            self.compileExpression()
            self.symbol_writer()
            self.advance()

        self.symbol_writer()

        self.advance()
        self.compileExpression()
        self.symbol_writer()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</letStatement>\n")
        self.advance()

    def compileWhile(self):
        """compile the While statement"""
        self.file_output.write(self.indentation() + "<whileStatement>\n")
        self.indent_count += 1
        self.keyword_writer()

        self.advance()
        self.symbol_writer()

        self.advance()
        self.compileExpression()

        self.symbol_writer()

        self.advance()
        self.symbol_writer()

        self.advance()
        self.compileStatements()

        self.symbol_writer()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</whileStatement>\n")
        self.advance()

    def compileReturn(self):
        """compile the Return statement"""
        self.file_output.write(self.indentation() + "<returnStatement>\n")
        self.indent_count += 1
        self.keyword_writer()

        self.advance()
        if self.TokenType() != self.SYMBOL and \
                self.symbol() != ";":
            self.compileExpression()

        self.symbol_writer()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</returnStatement>\n")
        self.advance()

    def compileIf(self):
        """compile the If statement"""
        self.file_output.write(self.indentation() + "<ifStatement>\n")
        self.indent_count += 1
        self.keyword_writer()

        self.advance()
        self.symbol_writer()

        self.advance()
        self.compileExpression()

        self.symbol_writer()

        self.advance()
        self.symbol_writer()

        self.advance()
        self.compileStatements()

        self.symbol_writer()

        self.advance()
        if self.TokenType() == self.KEYWORD() and self.keyword() == "else":
            self.keyword_writer()

            self.advance()
            self.symbol_writer()

            self.advance()
            self.compileStatements()

            self.symbol_writer()
            self.advance()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</ifStatement>\n")

    def compileExpression(self):
        """compile the Expression statement"""
        self.file_output.write(self.indentation() + "<expression>\n")
        self.indent_count += 1

        self.compileTerm()
        while self.TokenType() == self.SYMBOL() and \
                self.symbol() in OPERATIONS.keys():
            self.symbol_writer()
            self.advance()
            self.compileTerm()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</expression>\n")

    def compileTerm(self):
        """compile the Term statement"""
        bool_check = True
        self.file_output.write(self.indentation() + "<term>\n")
        self.indent_count += 1
        if self.TokenType() == self.KEYWORD():
            self.keyword_writer()
        elif self.TokenType() == self.STRING_CONST():
            self.string_const_writer()
        elif self.TokenType() == self.INT_CONST():
            self.integer_const_writer()
        elif self.symbol() == "(":
            self.symbol_writer()
            self.advance()
            self.compileExpression()
            self.symbol_writer()
        elif self.symbol() == "~" or self.symbol() == "-":
            self.symbol_writer()
            self.advance()
            self.compileTerm()
            bool_check = False
        elif self.TokenType() == self.IDENTIFIER():
            self.identifier_writer()
            self.advance()
            bool_check = False
            if self.symbol() == "[":
                bool_check = True
                self.symbol_writer()
                self.advance()
                self.compileExpression()
                self.symbol_writer()
            elif self.symbol() == ".":
                bool_check = True
                self.symbol_writer()
                self.advance()
                self.identifier_writer()
                self.advance()
                self.symbol_writer()
                self.advance()
                self.compileExpressionList()
                self.symbol_writer()
            elif self.symbol() == "(":
                bool_check = True
                self.symbol_writer()
                self.advance()
                self.compileExpressionList()
                self.symbol_writer()

        if bool_check:
            self.advance()
        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</term>\n")

    def compileExpressionList(self):
        """compile the ExpressionList"""
        self.file_output.write(self.indentation() + "<expressionList>\n")
        self.indent_count += 1

        if self.TokenType() != self.SYMBOL() and self.symbol() != ")":
            self.compileExpression()
            while self.TokenType() == self.SYMBOL() and self.symbol() == ",":
                self.symbol_writer()
                self.advance()
                self.compileExpression()
        if self.symbol() == "(":
            self.compileExpression()
            while self.TokenType() == self.SYMBOL() and self.symbol() == ",":
                self.symbol_writer()
                self.advance()
                self.compileExpression()

        self.indent_count -= 1
        self.file_output.write(self.indentation() + "</expressionList>\n")

    def compile_type_variable(self):
        """compile type and variable """
        if self.TokenType() == self.IDENTIFIER():
            self.identifier_writer()
        elif self.TokenType() == self.KEYWORD():
            self.keyword_writer()
        self.advance()
        self.identifier_writer()
        self.advance()
        while self.symbol() == ",":
            self.symbol_writer()
            self.advance()
            self.identifier_writer()
            self.advance()
        self.symbol_writer()
        self.advance()

    def identifier_writer(self):
        self.file_output.write(self.indentation() + "<identifier> " + self.identifier() + " </identifier>\n")

    def keyword_writer(self):
        """Writes the current keyword to the output file"""
        self.file_output.write(self.indentation() + "<keyword> " + self.keyword() + " </keyword>\n")

    def symbol_writer(self):
        """Writes the current symbol to the output file, handling special characters like <, > and & """
        write = self.symbol()
        if self.symbol() == "<":
            write = "&lt;"
        elif self.symbol() == "&":
            write = "&amp;"
        elif self.symbol() == ">":
            write = "&gt;"
        self.file_output.write(self.indentation() + "<symbol> " + write + " </symbol>\n")

    def integer_const_writer(self):
        """Writes the current integer constant to the output file"""
        self.file_output.write(self.indentation() + "<integerConstant> " + self.identifier() + " </integerConstant>\n")

    def string_const_writer(self):
        """Writes the current string constant to the output file"""
        self.file_output.write(self.indentation() + "<stringConstant> " + self.identifier() + " </stringConstant>\n")

    def compile_expression_list(self, jack_subroutine):
        """Compile a subroutine call expression_list"""
        # Handle expression list, so long as there are expressions
        count = 0  # Count expressions
        token = self.current_token()
        while token != ('symbol', ')'):

            if token == ('symbol', ','):
                self.tokenizer.advance()

            count += 1
            self.compile_expression(jack_subroutine)
            token = self.current_token()

        return count

    def compile_expression(self, jack_subroutine):
        """Compile an expression"""
        self.compile_term(jack_subroutine)

        token = self.current_token()
        while token.value in '+-*/&|<>=':
            binary_op = self.tokenizer.advance().value

            self.compile_term(jack_subroutine)
            self.vm_writer.write(OPERATIONS[binary_op])

            token = self.current_token()

    def compile_term(self, jack_subroutine):
        """Compile a term as part of an expression"""

        token = self.tokenizer.advance()
        # In case of unary operator, compile the term after the operator
        if token.value in ['-', '~']:
            self.compile_term(jack_subroutine)
            if token.value == '-':
                self.vm_writer.write('neg')
            elif token.value == '~':
                self.vm_writer.write('not')
        # In case of opening parenthesis for an expression
        elif token.value == '(':
            self.compile_expression(jack_subroutine)
            self.tokenizer.advance()  # )
        elif token.type == 'integerConstant':
            self.vm_writer.write_int(token.value)
        elif token.type == 'stringConstant':
            self.vm_writer.write_string(token.value)
        elif token.type == 'keyword':
            if token.value == 'this':
                self.vm_writer.write_push('pointer', 0)
            else:
                self.vm_writer.write_int(0)  # null / false
                if token.value == 'true':
                    self.vm_writer.write('not')

        # In case of a function call or variable name
        elif token.type == 'identifier':
            # Save token value as symbol and function in case of both
            token_value = token.value
            token_var = jack_subroutine.get_symbol(token_value)

            token = self.current_token()
            if token.value == '[':  # Array
                self.tokenizer.advance()  # [
                self.compile_expression(jack_subroutine)
                self.vm_writer.write_push_symbol(token_var)
                self.vm_writer.write('add')
                # rebase 'that' to point to var+index
                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('that', 0)
                self.tokenizer.advance()  # ]
            else:
                # Default class for function calls is this class
                func_name = token_value
                func_class = jack_subroutine.jack_class.name
                # Used to mark whether to use the default call, a method one
                default_call = True
                arg_count = 0

                if token.value == '.':
                    default_call = False
                    self.tokenizer.advance()  # .
                    # try to load the object of the method
                    func_obj = jack_subroutine.get_symbol(token_value)
                    func_name = self.tokenizer.advance().value  # function name
                    # If this is an object, call as method
                    if func_obj:
                        func_class = token_var.type  # Use the class of the object
                        arg_count = 1  # Add 'this' to args
                        self.vm_writer.write_push_symbol(token_var)  # push "this"
                    else:
                        func_class = token_value
                    token = self.current_token()

                # If in-fact a function call
                if token.value == '(':
                    if default_call:
                        # Default call is a method one, push this
                        arg_count = 1
                        self.vm_writer.write_push('pointer', 0)

                    self.tokenizer.advance()  # (
                    arg_count += self.compile_expression_list(jack_subroutine)
                    self.vm_writer.write_call(func_class, func_name, arg_count)
                    self.tokenizer.advance()  # )
                # If a variable instead
                elif token_var:
                    self.vm_writer.write_push_symbol(token_var)
