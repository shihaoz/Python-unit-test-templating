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

    def addBlock(self, name, new_block):
        self.blocks[name] = new_block


def searchScope(next_line, stream, indent_level, this_block):
    line = next_line
    while True:
        ''' end of file/end of scope: return line '''
        if line == '' or line.count(char_tab) < indent_level:
            return line
        ''' new scope: enter new scope '''
        if line.find('class ') and line.find(':'):
            next_line = str(line)
            line.lstrip()
            new_block = Block(line[line.find(' ')+1, line.find(':')])
            this_block.addBlock(new_block)
            # enter the new scope, with the new block
            line = searchScope(next_line=next_line, stream=stream, indent_level=indent_level+1, this_block=new_line)
            continue
        ''' a function: collect the function and save it to this_block '''
        line = line.strip()
        if line.find('def ') and line.find('(') and line.find(')')
            and line.find(':'): # this is a function definition
                # stores the lines and name of the function
                func = line
                name = line[line.find(' ')+1 : line.find('(')]
                line = stream.readline()
                while line.count(char_tab) >= (indent_level + 1):
                    # keep reading in
                    # todo: deal with a nested function
                    func += line
                    line = stream.readline()
                # stores the function
                this_block.addMethod(name, func)
                continue
        line = stream.readline()
        continue






""" end of file """
