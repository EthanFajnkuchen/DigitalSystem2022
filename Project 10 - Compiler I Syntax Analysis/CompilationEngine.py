from JackTokenizer import JackTokenizer

OPERATIONS = ["+", "-", "*", "/", "&", "|", "<", ">", "="]


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

    def compileClass(self):
        """
        Compiles a complete class.
        """
        if self.tokenizer.hasMoreTokens():
            self.indent_count += 1
            self.advance()
            self.file_output.write("<class>\n")
            self.keyword_writer()
            self.advance()
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
                self.symbol() in OPERATIONS:
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
