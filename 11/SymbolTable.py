class SymbolTable:
    _static_symbols = {}
    STATIC = 0
    FIELD = 0
    ARG = 0
    VAR = 0

    def __init__(self):
        self.FIELD = 0

        self.var_argument_symbols = {}
        self._field_symbols = {}

    def reset(self):
        self.var_argument_symbols = {}
        self.ARG = 0
        self.VAR = 0

    def define(self, name, type, kind):

        if kind == 'ARG':
            counter = self.ARG
            self.ARG += 1
            self.var_argument_symbols[name] = (type, kind, counter)
        elif kind == 'VAR':
            counter = self.VAR
            self.VAR += 1
            self.var_argument_symbols[name] = (type, kind, counter)
        elif kind == 'STATIC':
            counter = self.STATIC
            self.STATIC += 1
            self._static_symbols[name] = (type, kind, counter)
        elif kind == 'FIELD':
            counter = self.FIELD
            self.FIELD += 1
            self._field_symbols[name] = (type, kind, counter)

    def varCount(self, kind):
        if kind == 'VAR':
            return self.VAR
        elif kind == 'ARG':
            return self.ARG
        elif kind == 'STATIC':
            return self.STATIC
        elif kind == 'FIELD':
            return self.FIELD
        return None

    def kindOf(self, name):
        if name in self.var_argument_symbols.keys():
            return self.var_argument_symbols[name][1]
        elif name in self._field_symbols.keys():
            return self._field_symbols[name][1]
        elif name in self._static_symbols.keys():
            return self._static_symbols[name][1]
        else:
            return None

    def typeOf(self, name):
        if name in self.var_argument_symbols.keys():
            return self.var_argument_symbols[name][0]
        elif name in self._field_symbols.keys():
            return self._field_symbols[name][0]
        elif name in self._static_symbols.keys():
            return self._static_symbols[name][0]
        else:
            return None

    def indexOf(self, name):
        if name in self.var_argument_symbols.keys():
            return self.var_argument_symbols[name][2]
        elif name in self._field_symbols.keys():
            return self._field_symbols[name][2]
        elif name in self._static_symbols.keys():
            return self._static_symbols[name][2]
        else:
            return None
