import re


class Tokenizer:

    def __init__(self, file_path, xml_file):
        self.input_file = open(file_path, "r")
        self.current_index = 0
        self.current_command = ""
        self.commands = []
        self.xml_file = xml_file
        self.dictionary = {
            "KEYWORDS": r'^(class|constructor|method|function|field|static|var|int|char|boolean|void|true|false|null'
                        r'|this '
                        r'|let|do|if|else|while|return)$',
            "SYMBOLS": r'^({|}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||<|>|=|-|~)$',
            "INTS": r'^\d+$',
            "STRINGS": r'^"[^"\n\r]*"$',
            "IDENTIFIER": r'^[a-zA-Z]+[a-zA-Z_0-9]*$',
        }

    def has_more_lines(self):
        return not self.input_file.eof()

    def delete_comments(self):
        while '/**' in self.current_line:
            while not self.end_of_file and '*/' not in self.current_line:
                self.current_line = self.input_file.readline().strip()
            if not self.has_more_lines():
                return None
            self.current_line = self.current_line.replace(r'/\*\*.*\*\/', '')
            self.current_line = self.current_line.replace(r'.*\*\/', '')

    def line_advance(self):
        while self.has_more_lines():
            self.current_line = self.input_file.readline().strip().replace(r'(\/\/.*)|\r|\n', '')
            self.delete_comments()
            if self.current_line and not self.current_line.empty():
                return self.current_line
        return None

    def end_of_file(self):
        return not self.has_more_lines() and (self.commands and self.current_index == len(self.commands))

    def advance(self):
        if self.current_index == len(self.commands):
            if not self.line_advance():
                return None
            self.current_index = 0
            self.split_line()
        self.current_index += 1
        return self.current_command == self.commands[self.current_index - 1]

    def write_command(self):
        while not self.current_command:
            self.advance()
        self.xml_file.write("<{}> ".format(self.command_type()))
        if '"' in self.current_command:
            self.xml_file.write(self.current_command[1:-1])
        elif self.current_command == "<":
            self.xml_file.write("&lt;")
        elif self.current_command == ">":
            self.xml_file.write("&gt;")
        elif self.current_command == "&":
            self.xml_file.write("&amp;")
        else:
            self.xml_file.write(self.current_command)
        self.xml_file.write(" </{}>\n".format(self.command_type()))

    def command_type(self):
        keys = self.dictionary.keys();
        if re.match("KEYWORDS" in keys, self.current_command):
            return "keyword"
        elif re.match("SYMBOLS" in keys, self.current_command):
            return "symbol"
        elif re.match("INTS" in keys, self.current_command):
            return "integerConstant"
        elif re.match("STRINGS" in keys, self.current_command):
            return "stringConstant"
        else:
            return "identifier"

    def command_seg(self):
        if self.current_command == "class":
            return "class"
        elif self.current_command in ["static", "field"]:
            return "classVarDec"
        elif self.current_command in ["constructor", "function", "method"]:
            return "subroutineDec"
        elif self.current_command == "var":
            return "varDec"
        elif self.current_command in ["if", "while", "do", "return", "let"]:
            return "statements"
        else:
            return "else"

    def write_token_file(self):
        while not self.end_of_file():
            self.advance()
            self.write_command()
        self.xml_file.close()
        self.close()

    def close(self):
        self.input_file.close()

    def split_line(self):
        self.commands = self.split_symbols(self.current_line)

    def split_symbols(self, string):
        i = 0
        res = []
        strings = re.split(r'(")', string)
        while i < len(strings):
            if strings[i] == '"':
                if strings[i + 1] != '"':
                    res.append('"' + strings[i + 1] + '"')
                    i += i
                i += 1
            else:
                res.append(re.split(r' |({|}|\(|\)|\[|\]|\.|\,|\;|\+|\-|\*|\/|\&|\||<|>|=|-|~)', strings[i]))
            i += 1
        return [x for x in res if x != '']
