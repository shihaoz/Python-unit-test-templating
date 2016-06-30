from sys import platform as os_platform
from enum import Enum

char_tab = '\t'
new_line = ('\n' if os_platform == 'win32' else '\n')
ddt_method = char_tab + '@data(' + new_line*2 \
             + char_tab + ')' + new_line \
             + char_tab + '@unpack' + new_line
"""
Rule:  (newline = newline character, new line = an empty line)
    1. doc, body stores in the model will not have newline at the end or beginning.
    2. every model will have one newline at the end

"""


class TestType(Enum):
    Class = 1
    Function = 2

class TestBase:
    def __init__(self, _name, _args_list, _indent):
        self.type = None
        self.name = _name
        self.arguments = _args_list
        self.head = ''  # declaration line, set in derived class
        self.doc = ''  # documentation
        self.body = 'pass'  # method body
        self.indent_level = _indent
        self.ddt = False

    def toString(self):
        """
            return the head + doc + body
            will only have one newline at the end.
        """
        ret = (ddt_method if self.ddt and (self.type == TestType.Function) else "")\
            + self.indent_level * char_tab + self.head + new_line
        if len(self.doc) > 0:
            lines = self.doc.split(new_line)
            for line in lines:
                ret += (self.indent_level+1) * char_tab + line + new_line  # append newline

        if len(self.body) > 0:
            lines = self.body.split(new_line)
            for line in lines:
                ret += (self.indent_level+1) * char_tab + line + new_line  # append newline
        return ret

    def set_ddt(self):
        self.ddt = True

    def set_type(self, type: TestType):
        self.type = type

    def setDoc(self, _doc):
        """
        @require: the quotes will be added if not
        """
        if len(_doc) == 0:
            return self
        _doc.strip()
        self.doc = '"""' + new_line + _doc + new_line + '"""'
        return self

    def setBody(self, _body):
        self.body = _body
        self.body.strip()
        return self

    def addBody(self, _body):
        self.body += _body
        self.body.strip()
        return self

""" >>>>>>>>>>>>>>>>>>> """


class TestFunction(TestBase):
    """
        the unittest function template, each TestFunction represents one
        method/function to be tested
    """
    def __init__(self, _name : str, args, utility=False):
        super().__init__(_name.lower(), _args_list=args, _indent=1)
        self.set_type(TestType.Function)
        # define the declaration line
        self.head = 'def ' + ('test_' if utility==False else '')\
                    + '{}'.format(self.name)
        arguments = ', '.join(self.arguments)
        if len(self.arguments) > 0:
            if "self" not in arguments:
                self.head += '(self, {}, expected_output=None):'\
                    .format(arguments)
            else:
                self.head += '({}, expected_output=None):'.format(arguments)
        else:
            self.head += '(self, expected_output=None):'
        self.head.strip()
        self.setBody(_body='pass')

""" <<<<<<<<<<<<<<<<<<< """


class TestClass(TestBase):
    """
        the unittest class template,  one per module
    """
    def __init__(self, _name, args=[], ddt=False, pretty_printer=False, pretty_printer_indent=0):
        super().__init__(_name, _args_list=args, _indent=0)
        self.set_type(TestType.Class)
        self.methods = {}  # all the test_XXX methods
        self.head = 'class Test{}Methods(unittest.TestCase):'.format(_name)
        self.body = ''
        # adding startUp/tearDown function
        self.utility = {'startUp': TestFunction('startUp', [], utility=True),
                        'tearDown': TestFunction('tearDown', [], utility=True)
                        }

        # ddt option
        if ddt:
            self.set_ddt()
            self.head = '@ddt' + new_line + self.head

        # pretty printer option
        if pretty_printer:
            self.utility['startUp'].setDoc(' printer: a pretty_printer ')
            self.utility['startUp'].setBody('self.printer = pprint.PrettyPrinter(indent={}).pprint'
                                            .format(pretty_printer_indent))

    def toString(self):
        """
            return a string that is the template file of target module.
            returned string will be write to 'ut_XXX.py'
        """
        ret = super().toString() + new_line
        for func in self.utility.values():
            ret += func.toString() + new_line
        for method in self.methods.values():
            ret += method.toString() + new_line
        ret += '""" end of file """' + new_line*1
        return ret

    def addMethod(self, test_func):
        """
            add a new method to this TestClass
        """
        if not isinstance(test_func, TestFunction):
            raise TypeError('TestFunction type required: {}'.format(test_func.__class__))
        self.methods[test_func.name] = test_func
        if self.ddt:
            test_func.set_ddt()

    def setBody(self, body):
        raise ValueError('Class has no body to set')

    def addBody(self, body):
        raise ValueError('Class has no body to set')


""" end of file """
