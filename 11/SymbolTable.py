class SymbolTable:
    """A Jack class representation for the Jack compiler"""

    def __init__(self):
        self.symbols = [[]]  # list of lists ["name", "type", "kind", "#"]
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
        self.symbols = [[]]  # list of lists ["name", "type", "kind", "#"]
        self.static_symbols = 0
        self.field_symbols = 0
        self.argument_symbols = 0
        self.var_symbols = 0

    def define(self, name, type, kind):
        self.symbols.append([name, type, kind, self.what_kind(kind)])

    def varCount(self, kind) -> int:
        if kind == "STATIC":
            return self.static_symbols
        elif kind == "FIELD":
            return self.field_symbols
        elif kind == "ARG":
            return self.argument_symbols
        elif kind == "VAR":
            return self.var_symbols

    def kindOf(self, name) -> str:
        for raw in self.symbols:
            if raw.index(0) == name:
                return raw.index(2)

    def typeOf(self, name) -> str:
        for raw in self.symbols:
            if raw.index(0) == name:
                return raw.index(1)

    def indexOf(self, name) -> int:
        for raw in self.symbols:
            if raw.index(0) == name:
                return raw.index(3)
