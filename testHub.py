from TestModels import TestFunction, TestClass

test1 = TestFunction(_name='convert_from_dict', args=['user_dict', 'holder'])
# print('before doc: ')
# print(test1.toString())

test1.setDoc('convert from User Dictionary format into User object')
# print('after doc: ')
# print(test1.toString())

cls1 = TestClass('UserModel',ddt=True,
    pretty_printer=True, pretty_printer_indent=1)
cls1.setDoc('This is a preliminary documentation\n\tlol')
cls1.addDoc(' but here is more with an endline\n')
cls1.addMethod(test1)

try:
    cls1.addMethod('hi')
except TypeError:
    pass
try:
    cls1.addBody('asdas')
except ValueError:
    pass
try:
    cls1.setBody('asdas')
except ValueError:
    pass

print(cls1.toString())
