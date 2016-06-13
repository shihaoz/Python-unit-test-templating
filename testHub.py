from templateComponent import TestFunction, TestClass

test1 = TestFunction('convert_from_dict', ['user_dict', 'holder'])
# print('before doc: ')
# print(test1.toString())

test1.setDoc('convert from User Dictionary format into User object')
# print('after doc: ')
# print(test1.toString())

cls1 = TestClass('UserModel',ddt=True,
    pretty_printer=True, pretty_printer_indent=1)
cls1.addMethod(test1)
print(cls1.toString())
