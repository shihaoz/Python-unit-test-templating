from sys import platform as os_platform
import io


char_tab = '\t'
new_line = ('\r\n' if os_platform == 'win32' else '\n')

class TestBase:
    def __init__(self, _name, _args_list, _indent):
        self.name = _name
        self.arguments = _args_list
        self.head = '' # declaration line, set in derived class
        self.doc = '' # documentation
        self.body = 'pass' # method body
        self.indent_level = _indent

    def toString(self):
        """
            return the head + doc + body
            depends on indent_level
            inject number of tabs into print
        """
        ret = self.indent_level * char_tab + self.head + new_line

        docIO = io.StringIO(self.doc)
        for line in docIO:
            ret += (self.indent_level+1) * char_tab + line  # line has \n at the end

        bodyIO = io.StringIO(self.body)
        for line in bodyIO:
            ret += (self.indent_level+1) * char_tab + line  # line has \n at the end
        ret += new_line
        return ret

    def setDoc(self, _doc):
        """
        @require: the quotes will be added if not
        """
        if _doc[-1] != new_line:
            _doc = _doc + new_line
        if _doc.find('"""') == -1:
            self.doc = '"""' + new_line + '{doc}"""'.format(_doc)
        else:
            self.doc = _doc
        return self


    def setBody(self, _body):
        self.body = _body
        return self


    def addBody(self, _body):
        self.body += _body
        return self

""" >>>>>>>>>>>>>>>>>>> """

class TestFunction(TestBase):
    """
        the unittest function template, each TestFunction represents one
        method/function to be tested
    """
    def __init__(self, _name, args, utility=False):
        super().__init__(_name, _args_list=args, _indent=1)
        # define the declaration line
        self.head = 'def ' + ('test_' if utility==False else '')\
                    + '{}'.format(self.name)
        if len(self.arguments) > 0:
            self.head += '(self, {}, expected_output=None):'\
                .format(', '.join(self.arguments))
        else:
            self.head += '(self, expected_output=None):'
        self.body = 'pass'
        return self

""" <<<<<<<<<<<<<<<<<<< """

class TestClass(TestBase):
    """
        the unittest class template,  one per module
    """
    def __init__(self, _name, args=[], ddt=False, pretty_printer=False, pretty_printer_indent=0):
        super().__init__(_name, _args_list=args, _indent=0)
        self.methods = {} # all the test_XXX methods
        self.head = 'class Test{}Methods(unittest.TestCase):'.format(_name)
        self.body = ''
        # adding startUp/tearDown function
        self.utility = {'startUp': TestFunction('startUp', [], utility=True),
                        'tearDown': TestFunction('tearDown', [], utility=True)
                        }


        # ddt option
        if ddt:
            self.ddt_method = (self.indent_level+1) * char_tab + '@data(' + new_line
            + (self.indent_level+1) * char_tab + ')' + new_line
            + (self.indent_level+1) * char_tab + '@unpack' + new_line
            self.head = '@ddt' + new_line + self.head

        # pretty printer option
        if pretty_printer:
            self.utility['startUp'].setDoc(' printer: a pretty_printer ' + new_line)
            self.utility['startUp'].setBody('self.printer = pprint.PrettyPrinter(indent={}).pprint'
                .format(pretty_printer_indent))

    def toString(self):
        """
            return a string that is the template file of target module.
            returned string will be write to 'ut_XXX.py'
        """
        ret = super().toString()
        for func in self.utility.values():
            ret += func.toString() + new_line
        for method in self.methods.values():
            ret += method.toString() + new_line

        ret += new_line*2 + '""" end of file """' + new_line*2
        return ret

    def addMethod(self, test_func):
        """
            add a new method to this TestClass
        """
        if not isinstance(test_func, TestFunction):
            raise TypeError('TestFunction type required: {}'.format(test_func.__class__))
        self.methods[test_func.name] = test_func

    def setBody(self, body):
        raise ValueError('Class has no body to set')
    def addBody(self, body):
        raise ValueError('Class has no body to set')


""" end of file """
