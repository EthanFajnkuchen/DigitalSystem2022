class Code(object):
    def dest(self, dest):
        DictionaryDest = {
            None: '000',
            'M': '001',
            'D': '010',
            'DM': '011',
            'A': '100',
            'AM': '101',
            'AD': '110',
            'ADM': '111',
        }
        return DictionaryDest.get(dest, '000')  # return the destination from the dictionaries

    def comp(self, comp):
        DictionaryComp = {
            '0': '101010',
            '1': '111111',
            '-1': '111010',
            'D': '001100',
            'A': '110000',
            '!D': '001101',
            '!A': '110001',
            '-D': '001111',
            '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101',
        }
        address = '0'
        if 'M' in comp:  # check if A or M is in the comp
            address = '1'
            comp = comp.replace('M', 'A')  # replace the A and M by the dictionary initialization
        address += DictionaryComp.get(comp, '0000000')  # adding to the address the output from the dictionary
        return address

    def jump(self, jump):
        DictionaryJump = {
            None: '000',
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        return DictionaryJump.get(jump, '000')  # return the JUMP from the dictionaries


class SymbolTable(object):
    DictionarySymbolTable = {
        'R0': '000000000000000',
        'R1': '000000000000001',
        'R2': '000000000000010',
        'R3': '000000000000011',
        'R4': '000000000000100',
        'R5': '000000000000101',
        'R6': '000000000000110',
        'R7': '000000000000111',
        'R8': '000000000001000',
        'R9': '000000000001001',
        'R10': '000000000001010',
        'R11': '000000000001011',
        'R12': '000000000001100',
        'R13': '000000000001101',
        'R14': '000000000001110',
        'R15': '000000000001111',
        'SP': '000000000000000',
        'LCL': '000000000000001',
        'ARG': '000000000000010',
        'THIS': '000000000000011',
        'THAT': '000000000000100',
        'SCREEN': '100000000000000',
        'KBD': '110000000000000',
    }

    def __init__(self):
        self.dictionary = self.DictionarySymbolTable()  # initialize dictionary
        self.start = 16  # As the program start

    def addEntry(self, symbol, address):
        self.dictionary.update(self, {symbol, address}) #adding item to the dictionary

    def contains(self, symbol): #return boolean statment if the dictionary contain this symbol
        for s in self.dictionary:
            if s == symbol:
                return True
        return False

    def getAddress(self, symbol):
        return self.dictionary.get(symbol) #return the address from the input symbol
