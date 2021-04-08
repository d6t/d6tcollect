import d6tcollect
class MyClass0(object):
    @d6tcollect._collectClass
    def myfunction_1(self, num, another=5):
        return num ** 2

class MyClass1(MyClass0):
    pass
class MyClass2(MyClass1):
    pass

MyClass0().myfunction_1(1)
MyClass1().myfunction_1(1)
MyClass2().myfunction_1(1)
