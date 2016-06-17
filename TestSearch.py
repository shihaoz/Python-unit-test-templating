import re
import io
from TestModels import TestClass, TestFunction, new_line, char_tab

target_name = 'Sample/try.py'

"""
 a two stage process for building Test models:
    1. split the file into blocks and scopes
    2. build based on the blocks and scopes
"""

class Block:
    """
        a block represents an module with a tree-like hierarchy. each method
        is directly under this Block.
        Each Class within the module is another Block within the Block
        (think of Block as a group of methods that share the same indent level)
    """
    def __init__(self, name):
        self.methods = {}
        self.blocks = {}
        self.name = name

    def addMethod(self, name, method):
        self.methods[name] = method

    def addBlock(self, new_block):
        self.blocks[new_block.name] = new_block

    def toString(self):
        ret = self.name + new_line
        for k,v in self.methods.items():
            ret += '#function: {}\n{}'.format(k, v) + new_line
        for k,v  in self.blocks.items():
            ret += '#class: {}\n{}'.format(k, v.toString())
        return ret + '\n'


def blank_line(line):
    strip_line = str(line)
    strip_line = strip_line.strip()
    if len(strip_line) == 0 or strip_line[0] == '#':
        return True
    else:
        return False

def searchScope(next_line, stream, indent_level, this_block):
    this_line = next_line
    while True:
        ''' end of file/end of scope: return this_line '''
        if blank_line(this_line):
            return ''
        if this_line.count(' ') < indent_level:
            return this_line

        pattern = r'class [\w()]+:'
        if re.search(pattern, this_line) is not None:
            ''' new class: enter new scope '''
            name = re.search(r'class (\w+)', this_line).group()  # get the 'class Name'
            new_block = Block(name=name[name.find(' ') + 1:])
            this_block.addBlock(new_block)
            # enter the new scope, with the new block and the next_line
            this_line = stream.readline()
            this_line = searchScope(next_line=this_line, stream=stream, indent_level=indent_level+1, this_block=new_block)
            if blank_line(this_line):
                this_line = stream.readline()
            continue
        ''' a function: collect the function and save it to this_block '''
        this_line = this_line.strip()
        pattern = r'def \w+\([\w, ]+\):'  # match the def \w (\w, \w): form
        if re.search(pattern, this_line) is not None: # this is a function definition
                # stores the lines and name of the function
                function_body = this_line + new_line
                name = this_line[this_line.find(' ')+1: this_line.find('(')]   # get function name
                this_line = stream.readline()
                while this_line.count(' ') > indent_level:
                    # keep reading in
                    # todo: deal with a nested function
                    function_body += this_line
                    this_line = stream.readline()
                this_block.addMethod(name, function_body)  # stores the function body
                continue
        this_line = stream.readline()    # empty line





this_file = Block(name='simple.py')
with open('Sample/simple.py', 'r') as fstream:
    line = fstream.readline()
    searchScope(next_line=line, stream=fstream, indent_level=0, this_block=this_file)

with open('blocks.txt', 'w') as fstream:
    fstream.write(this_file.toString())

""" end of file """
