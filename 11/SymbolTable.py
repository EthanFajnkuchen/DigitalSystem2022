class SymbolTable:
    """A Jack class representation for the Jack compiler"""

    def __init__(self):
        self.static_field_symbols = []  # list of lists ["name", "type", "kind", "#"]
        self.var_argument_symbols = []  # list of lists ["name", "type", "kind", "#"]
        self.static_symbols = 0
        self.field_symbols = 0
        self.argument_symbols = 0
        self.var_symbols = 0

    def what_kind(self, kind) -> int:
        if kind == "STATIC":
            self.static_symbols += 1
            return self.static_symbols
        elif kind == "FIELD":
            self.field_symbols += 1
            return self.field_symbols
        elif kind == "ARG":
            self.argument_symbols += 1
            return self.argument_symbols
        elif kind == "VAR":
            self.var_symbols += 1
            return self.var_symbols

    def reset(self):
        self.var_argument_symbols = []  # list of lists ["name", "type", "kind", "#"]
        self.argument_symbols = 0
        self.var_symbols = 0

    def define(self, name: str, type: str, kind: str):
        kindness = self.what_kind(kind)
        if kind in ['STATIC', 'FIELD']:
            self.static_field_symbols.append([name, type, kind, kindness])
        else:
            self.var_argument_symbols.append([name, type, kind, kindness])

    def varCount(self, kind) -> int:
        if kind == "STATIC":
            return self.static_symbols
        elif kind == "FIELD":
            return self.field_symbols
        elif kind == "ARG":
            return self.argument_symbols
        elif kind == "VAR":
            return self.var_symbols

    def kindOf(self, name):
        symbols = self.static_field_symbols + self.var_argument_symbols
        for raw in symbols:
            if raw[0] == name:
                return raw[2]
        return None

    def typeOf(self, name):
        symbols = self.static_field_symbols + self.var_argument_symbols
        for raw in symbols:
            if raw[0] == name:
                return raw[1]
        return None

    def indexOf(self, name):
        symbols = self.static_field_symbols + self.var_argument_symbols
        for raw in symbols:
            if raw[0] == name:
                return raw[3]
        return None

    def printing(self):
        symbols = self.static_field_symbols + self.var_argument_symbols
        print(symbols)
        print('static')
        print(self.static_field_symbols)
        print('var')
        print(self.var_argument_symbols)
        for raw in symbols:
            print(raw)
