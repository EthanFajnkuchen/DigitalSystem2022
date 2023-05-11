import re


is_keyword = re.compile("^\s*(""class|constructor|function|method|static|field"
                              "|var|int|char|boolean|void|true|false|null|this|"
                              "let|do|if|else|while|return)\s*")

class JackTokenizer:


    keyword = ["CLASS",
               "METHOD",
               "FUNCTION",
               "CONSTRUCTOR",
               "INT",
               "BOOLEAN",
               "CHAR",
               "VOID",
               "VAR",
               "STATIC",
               "FIELD",
               "LET",
               "DO",
               "IF",
               "ELSE",
               "WHILE",
               "RETURN",
               "TRUE",
               "FALSE",
               "NULL",
               "THIS"]

    KEYWORD = 0
    SYMBOL = 1
    INT_CONST = 2
    STRING_CONST = 3
    IDENTIFIER = 4

    def __init__(self, input_file):
        with open(input_file, "r") as file:
            self.text = file.read()
        self.clear_comments()
        self._currentToken = None
        self._tokenType = None


    def clear_comments(self):
        self.text = re.sub("(//.*)|(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)", "", self.text)

    def hasMoreTokens(self):
        if re.fullmatch(re.compile("\s*"), self.text):
            return False
        return True

    def advance(self):
        if self.hasMoreTokens():
            if self.hasMoreTokens():
                token_types = [
                    (JackTokenizer.KEYWORD, is_keyword),
                    (JackTokenizer.SYMBOL, re.compile("^\s*([{}()\[\].,;+\-*/&|<>=~])\s*")),
                    (JackTokenizer.INT_CONST, re.compile("^\s*(\d+)\s*")),
                    (JackTokenizer.STRING_CONST, re.compile("^\s*\"(.*)\"\s*")),
                    (JackTokenizer.IDENTIFIER, re.compile("^\s*([a-zA-Z_][a-zA-Z1-9_]*)\s*"))
                ]

                for token_type, regex in token_types:
                    is_match = re.match(regex, self.text)
                    if is_match is not None:
                        self.text = re.sub(regex, "", self.text)
                        self._tokenType = token_type
                        self._currentToken = is_match.group(1)
                        break

    def tokenType(self):
        return self._tokenType

    def keyWord(self):
        return self._currentToken

    def symbol(self):
        return self._currentToken

    def identifier(self):
        return self._currentToken

    def intVal(self):
        return int(self._currentToken)

    def stringVal(self):
        return self._currentToken




