import re
import io
from TestModels import TestClass, TestFunction, new_line, char_tab

target_name = 'Sample/try.py'

# function pattern: def XXX(XXX, XX='', XX="", XX=XX.AA ):
pattern_function = 'def (\w+)\(([\w, =\'".]+)\):'
pattern_import = r'\bimport\b'
imports = ["import unittest",
           "from unittest.mock import patch, Mock, MagicMock",
           "from deepdiff import DeepDiff"]
ddt_import = "from ddt import ddt, data, unpack"
pprint_import = "import pprint"
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
    def __init__(self, name: str):
        self.methods = {}
        self.blocks = {}
        self.name = name[0: name.find('.')] if name.find('.') != -1 else name

    def addMethod(self, name, method):
        """
        :param name: name of the method
        :param method: method body
        :return:
        """
        self.methods[name] = method
        return self

    def addBlock(self, new_block):
        """
        :param new_block: a Block object within this block scope
        :return:
        """
        self.blocks[new_block.name] = new_block
        return self

    def toString(self):
        """ convert Block content to a string
        :return: a string that represents the block content
        """
        ret = self.name + new_line
        for k,v in self.methods.items():
            ret += '#function: {}\n{}'.format(k, v) + new_line
        for k,v in self.blocks.items():
            ret += '#class: {}\n{}'.format(k, v.toString())
        return ret + '\n'


def blank_line(line):
    strip_line = str(line)
    strip_line = strip_line.strip()
    if len(strip_line) == 0 or strip_line[0] == '#':
        return True
    else:
        return False

def valid_indent(line, indent, equal=False):
    if equal: # <=, used by function
        return False if line.count('    ') <= indent else True
    return False if line.count('    ') < indent else True

def search_scope(next_line, stream, indent_level, this_block):
    this_line = next_line
    while True:
        ''' end of file: return empty string '''
        if blank_line(this_line):
            return ''
        # end of scope: return this_line
        if not valid_indent(this_line, indent_level, equal=False):
            return this_line

        # if this is a class
        pattern = r'class (\w+)'
        match = re.search(pattern, this_line)
        if match is not None and this_line.find(':') != -1:  # a well-formed class
            ''' new class: enter new scope '''
            name = match.group(1)  # get the 'class Name'
            new_block = Block(name=name)
            this_block.addBlock(new_block)
            # enter the new scope, with the new block and the next_line
            this_line = search_scope(next_line=stream.readline(), stream=stream,
                                     indent_level=indent_level+1, this_block=new_block)
            if blank_line(this_line):
                this_line = stream.readline()
            continue

        # if this is a function
        pattern = pattern_function
        match = re.search(pattern, this_line)
        if match is not None:  # this is a function definition
                # stores the lines and name of the function
                name = match.group(1)  # get function name
                function_body = this_line.strip() + new_line

                this_line = stream.readline()
                while valid_indent(this_line, indent_level, equal=True):
                    # keep reading in
                    function_body += this_line.strip() + new_line
                    this_line = stream.readline()

                this_block.addMethod(name, function_body)  # stores the function body
                continue
        this_line = stream.readline()    # empty line


this_file = Block(name='complex.py')

with open('Sample/complex.py', 'r') as fstream:
    file = ''
    import_end = False
    for line in fstream:
        if not blank_line(line):
            if not import_end and re.search(pattern_import, line):
                imports.append(line.strip())
            else:
                import_end = True
                file += line
    with io.StringIO(file) as textStream:
        search_scope(next_line=textStream.readline(), stream=textStream, indent_level=0, this_block=this_file)


def break_function(function_body):
    """
    :param function_body: a valid function body (with declaration, doc, and body)
    :return: (name, args, doc)
    """
    lines = function_body.split(new_line)
    declaration = lines[0]
    match = re.search(pattern_function, declaration)
    name = match.group(1)
    args = [x.strip() for x in match.group(2).split(',')]  # strip whitespace from arguments

    idx, comment = (1, '')
    if lines[idx].find('"""') == -1:
        # no doc string
        return name, args, comment
    # has doc string
    idx += 1
    while lines[idx].find('"""') == -1:
        # find the enclosing """
        idx += 1
    for x in range(1, idx+1):  # from the first to the last line of comment
        comment += lines[x]
    comment = comment.strip()
    comment = comment.strip('"')
    return name, args, comment


def build_model(prefix: str, test_class : TestClass, this_block : Block):
    """

    :param prefix: prefix of name, if a method is within a class, then name == test_class_methodname
    :param test_model: a TestClass where u add the TestFunction
    :param this_block: a block
    :return: the test_model
    """
    for name, function in this_block.methods.items():
        (name, args, doc) = break_function(function_body=function)
        test_function = TestFunction(_name=prefix+name, args=args).setDoc(_doc=doc)
        test_class.addMethod(test_function)
    for name, block in this_block.blocks.items():
        test_class = build_model(prefix=name + '_', test_class=test_class, this_block=block)
    return test_class


# build functions with {name, args, doc}
# build class with {name, args, options}
pretty_printer = True
ddt = True
module = TestClass(_name=this_file.name, args=[], ddt=ddt, pretty_printer=pretty_printer, pretty_printer_indent=2)
if ddt:
    imports.append(ddt_import)
if pretty_printer:
    imports.append(pprint_import)

write_file = 'hold.py'

module = build_model(prefix='', test_class=module, this_block=this_file)
with open(write_file, 'w') as wstream:
    for line in imports:
        wstream.write(line + new_line)
    wstream.write(new_line)
    wstream.write(module.toString())
""" end of file """


'''
    work on importing files.
'''