from SymbolTable import SymbolTable
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter

OPERATIONS = {
    '+': 'ADD',
    '-': 'SUB',
    '=': 'EQ',
    '>': 'GT',
    '<': 'LT',
    '&': 'AND',
    '|': 'OR'
}


class CompilationEngine:
    KIND_SWITCHER = {
        'ARG': 'ARG',
        'STATIC': 'STATIC',
        'VAR': 'VAR',
        'FIELD': 'THIS'
    }

    if_counter = -1
    while_counter = -1

    def __init__(self, input_file, output_file):
        self.class_name = None
        self.vm_writer = VMWriter(output_file)
        self.tokenizer = JackTokenizer(input_file)
        self.symbol_table = SymbolTable()
        self.symbol_list = []

    def compileClass(self):
        self.get_token()
        self.class_name = self.get_token()
        self.get_token()

        while self.peek() in ['static', 'field']:
            self.compileClassVarDec()

        while self.peek() in ['constructor', 'function', 'method']:
            self.compileSubroutine()  # subroutineDec*

        self.vm_writer.close()

    def compileClassVarDec(self):
        kind = self.get_token()
        type = self.get_token()
        name = self.get_token()
        self.add_symbol(name, type, kind.upper())
        while self.peek() != ';':
            self.get_token()
            name = self.get_token()
            self.add_symbol(name, type, kind.upper())

        self.get_token()  # ;

    def compileSubroutine(self):
        subroutine_kind = self.get_token()
        self.get_token()
        subroutine_name = self.get_token()
        self.symbol_table.reset()

        if subroutine_kind == 'method':
            self.add_symbol('instance', self.class_name, 'ARG')

        self.get_token()  # (
        self.compileParameterList()
        self.get_token()  # )
        self.get_token()  # {

        while 'var' == self.peek():
            self.compileVarDec()

        function_name = '{}.{}'.format(self.class_name, subroutine_name)
        num_locals = self.symbol_table.varCount('VAR')
        self.vm_writer.write_function(function_name, num_locals)

        if subroutine_kind == 'constructor':
            num_fields = self.symbol_table.varCount('FIELD')
            self.vm_writer.write_push('CONST', num_fields)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('POINTER', 0)
        elif subroutine_kind == 'method':
            self.vm_writer.write_push('ARG', 0)
            self.vm_writer.write_pop('POINTER', 0)

        self.compileStatements()  # statements
        self.get_token()  # '}'

    def compileParameterList(self):
        if ')' != self.peek():
            type = self.get_token()
            name = self.get_token()

            self.add_symbol(name, type, 'ARG')

        while ')' != self.peek():
            self.get_token()  # ','

            type = self.get_token()  # type
            name = self.get_token()  # varName

            self.add_symbol(name, type, 'ARG')

    # 'var' type varName (',' varName)* ';'
    def compileVarDec(self):
        self.get_token()
        type = self.get_token()
        name = self.get_token()

        self.add_symbol(name, type, 'VAR')

        while self.peek() != ';':
            self.get_token()
            name = self.get_token()
            self.add_symbol(name, type, 'VAR')

        self.get_token()

    def compileStatements(self):
        while self.peek() in ['let', 'if', 'while', 'do', 'return']:
            token = self.get_token()

            if 'let' == token:
                self.compileLet()
            elif 'if' == token:
                self.compileIf()
            elif 'while' == token:
                self.compileWhile()
            elif 'do' == token:
                self.compileDo()
            elif 'return' == token:
                self.compileReturn()

    def compileDo(self):
        self.compile_subroutine_call()
        self.vm_writer.write_pop('TEMP', 0)
        self.get_token()  # ';'

    def compileLet(self):
        var_name = self.get_token()
        var_kind = self.KIND_SWITCHER[self.symbol_table.kindOf(var_name)]
        var_index = self.symbol_table.indexOf(var_name)

        if '[' == self.peek():
            self.get_token()  # [
            self.compileExpression()
            self.get_token()  # ]

            self.vm_writer.write_push(var_kind, var_index)

            self.vm_writer.write_arithmetic('ADD')
            self.vm_writer.write_pop('TEMP', 0)

            self.get_token()  # =
            self.compileExpression()
            self.get_token()  # ;

            self.vm_writer.write_push('TEMP', 0)
            self.vm_writer.write_pop('POINTER', 1)
            self.vm_writer.write_pop('THAT', 0)
        else:
            self.get_token()  # =
            self.compileExpression()
            self.get_token()  # ;

            self.vm_writer.write_pop(var_kind, var_index)

    def compileWhile(self):
        self.while_counter += 1
        while_index = self.while_counter

        self.vm_writer.write_label('WHILE{}\n'.format(while_index))

        self.get_token()  # (
        self.compileExpression()
        self.vm_writer.write_arithmetic('NOT')
        self.get_token()  # )
        self.get_token()  # {

        self.vm_writer.write_if('WHILE_END{}\n'.format(while_index))
        self.compileStatements()
        self.vm_writer.write_goto('WHILE{}\n'.format(while_index))
        self.vm_writer.write_label('WHILE_END{}\n'.format(while_index))

        self.get_token()  # }

    def compileReturn(self):
        if self.peek() != ';':
            self.compileExpression()
        else:
            self.vm_writer.write_push('CONST', 0)

        self.vm_writer.write_return()
        self.get_token()  # ;

    def compileIf(self):
        self.if_counter += 1
        if_index = self.if_counter

        self.get_token()  # (
        self.compileExpression()
        self.get_token()  # )

        self.get_token()  # {

        self.vm_writer.write_if('IF_TRUE{}\n'.format(if_index))
        self.vm_writer.write_goto('IF_FALSE{}\n'.format(if_index))
        self.vm_writer.write_label('IF_TRUE{}\n'.format(if_index))
        self.compileStatements()
        self.vm_writer.write_goto('IF_END{}\n'.format(if_index))

        self.get_token()  # }

        self.vm_writer.write_label('IF_FALSE{}\n'.format(if_index))

        if self.peek() == 'else':
            self.get_token()
            self.get_token()
            self.compileStatements()
            self.get_token()

        self.vm_writer.write_label('IF_END{}\n'.format(if_index))

    def compileExpression(self):
        self.compileTerm()
        keys = OPERATIONS.keys()
        while self.peek() in keys:
            token = self.get_token()
            self.compileTerm()
            if token in keys:
                self.vm_writer.write_arithmetic(OPERATIONS[token])
            elif token == '/':
                self.vm_writer.write_call('Math.divide', 2)
            elif token == '*':
                self.vm_writer.write_call('Math.multiply', 2)

    def compileTerm(self):
        if self.peek() in ['~', '-']:
            unary_op = self.get_token()
            self.compileTerm()
            if unary_op == "-":
                self.vm_writer.write_arithmetic("NEG")
            elif unary_op == "~":
                self.vm_writer.write_arithmetic("NOT")
        elif '(' == self.peek():
            self.get_token()  # (
            self.compileExpression()
            self.get_token()  # )
        elif self.peek_type() == 2:  # integer Const
            self.vm_writer.write_push('CONST', self.get_token())
        elif self.peek_type() == 3:  # string Const
            self.compile_string()
        elif self.peek_type() == 0:  # keyword Const
            self.compile_keyword()
        else:
            if self.is_array():
                array_var = self.get_token()

                self.get_token()  # [
                self.compileExpression()
                self.get_token()  # ]

                array_kind = self.symbol_table.kindOf(array_var)
                array_index = self.symbol_table.indexOf(array_var)
                self.vm_writer.write_push(self.KIND_SWITCHER[array_kind], array_index)

                self.vm_writer.write_arithmetic('ADD')
                self.vm_writer.write_pop('POINTER', 1)
                self.vm_writer.write_push('THAT', 0)
            elif self.is_subroutine_call():
                self.compile_subroutine_call()
            else:
                var = self.get_token()
                var_kind = self.KIND_SWITCHER[self.symbol_table.kindOf(var)]
                var_index = self.symbol_table.indexOf(var)
                self.vm_writer.write_push(var_kind, var_index)

    def compileExpressionList(self):
        number_args = 0

        if ')' != self.peek():
            number_args += 1
            self.compileExpression()

        while ')' != self.peek():
            number_args += 1
            self.get_token()  # ,
            self.compileExpression()

        return number_args

    def compile_keyword(self):
        keyword = self.get_token()  # keyword Const

        if keyword == 'this':
            self.vm_writer.write_push('POINTER', 0)
        else:
            self.vm_writer.write_push('CONST', 0)

            if keyword == 'true':
                self.vm_writer.write_arithmetic('NOT')

    def compile_subroutine_call(self):
        identifier = self.get_token()
        function_name = identifier
        number_args = 0

        if '.' == self.peek():
            self.get_token()  # '.'
            subroutine_name = self.get_token()

            type = self.symbol_table.typeOf(identifier)

            if type is not None:
                instance_kind = self.symbol_table.kindOf(identifier)
                instance_index = self.symbol_table.indexOf(identifier)
                self.vm_writer.write_push(self.KIND_SWITCHER[instance_kind], instance_index)

                function_name = '{}.{}'.format(type, subroutine_name)
                number_args += 1
            else:
                class_name = identifier
                function_name = '{}.{}'.format(class_name, subroutine_name)
        elif '(' == self.peek():
            subroutine_name = identifier
            function_name = '{}.{}'.format(self.class_name, subroutine_name)
            number_args += 1

            self.vm_writer.write_push('POINTER', 0)

        self.get_token()  # (
        number_args += self.compileExpressionList()
        self.get_token()  # )

        self.vm_writer.write_call(function_name, number_args)

    def compile_string(self):
        string = self.get_token()  # string Cons

        self.vm_writer.write_push('CONST', len(string))
        self.vm_writer.write_call('String.new', 1)

        for char in string:
            self.vm_writer.write_push('CONST', ord(char))
            self.vm_writer.write_call('String.appendChar', 2)

    def is_subroutine_call(self):
        token = self.get_token()
        subroutine_call = self.peek() in ['.', '(']
        self.symbol_list.insert(0, (token, 'UNKNOWN'))
        return subroutine_call

    def is_array(self):
        token = self.get_token()
        array = self.peek() == '['
        self.symbol_list.insert(0, (token, 'UNKNOWN'))
        return array

    def peek(self):
        if self.symbol_list:
            token_info = self.symbol_list.pop(0)
        else:
            token_info = self.next()
        self.symbol_list.insert(0, token_info)
        return token_info[0]

    def peek_type(self):
        if self.symbol_list:
            token_info = self.symbol_list.pop(0)
        else:
            token_info = self.next()
        self.symbol_list.insert(0, token_info)
        return token_info[1]

    def get_token(self):
        if self.symbol_list:
            name = self.symbol_list.pop(0)[0]
            return name
        else:
            token = self.next()
            return token[0]

    def next(self):
        if self.tokenizing_exist():
            self.tokenizer.advance()
            token_type = self.token_type()
            if token_type == 0:
                return self.tokenizer.keyWord().lower(), token_type
            elif token_type == 4:
                return self.tokenizer.identifier(), token_type
            elif token_type == 1:
                return self.tokenizer.symbol(), token_type
            elif token_type == 3:
                return self.tokenizer.stringVal(), token_type
            elif token_type == 2:
                return self.tokenizer.intVal(), token_type
        return None, None

    def add_symbol(self, name, type, kind):
        self.symbol_table.define(name, type, kind)

    def token_type(self):
        return self.tokenizer.tokenType()

    def tokenizing_exist(self):
        return self.tokenizer.hasMoreTokens()
