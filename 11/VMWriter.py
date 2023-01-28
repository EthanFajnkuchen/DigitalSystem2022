class VMWriter:
    """A jack to VM writer, used by the compiler to output the code matching
    to the analyzed code"""

    def __init__(self, output):
        """Initialize the VMWriter with a given output stream"""
        self.output = open(output, "w+")

    def write_if(self, label):
        """Write an if-goto used in while/if.
        used to jump to label if the condition *doesn't* hold"""
        self.output.write('not\n')  # Negate to jump if the conditions doesn't hold
        self.output.write('if-goto {}\n'.format(label))

    def write_goto(self, label):
        """Write a goto for the VM"""
        self.output.write('goto {}\n'.format(label))

    def write_label(self, label):
        """Write a label in VM"""
        self.output.write('label {}\n'.format(label))

    def write_function(self, name, nVars):
        """Write a function header for a Jack subroutine"""
        self.output.write('function {}.{} \n'.format(name, nVars))

    def write_return(self):
        """Write the return statement"""
        self.output.write('return\n')

    def write_call(self, func_name, arg_count):
        """Write a call to a function with n-args"""
        self.output.write('call {0}.{1} \n'.format(func_name, arg_count))

    def write_pop(self, segment, offset):
        if segment == 'CONST':
            segment = 'constant'
        elif segment == 'ARG':
            segment = 'argument'
        elif segment == 'VAR':
            segment = 'local'
        """Pop the value in the top of the stack to segment:offset"""
        self.output.write('pop {0} {1}\n'.format(segment.lower(), offset))

    def write_push(self, segment, offset):
        if segment == 'CONST':
            segment = 'constant'
        elif segment == 'ARG':
            segment = 'argument'
        elif segment == 'VAR':
            segment = 'local'
        """Push the value to the stack from segment:offset"""
        self.output.write('push {0} {1}\n'.format(segment.lower(), offset))

    def write_arithmetic(self, command):
        self.output.write('{0}\n'.format(command.lower()))

    def close(self):
        self.output.close()
