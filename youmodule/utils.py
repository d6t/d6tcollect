import d6tcollect
d6tcollect.init(__name__)

class MyClass0(object,metaclass=d6tcollect.Collect):
    @d6tcollect._collectClass
    def __init__(self, *args, **kwargs):
        self.___init__()

    def ___init__(self):
        pass

    def myfunction_1(self, num, another=5):
        return num ** 2

class MyClass(MyClass0,metaclass=d6tcollect.Collect):
    def myfunction_2(self, arg):
        return arg ** 3

    def myfunction_3(self, arg):
        return arg / 0



class MyClass1(object):
    @d6tcollect._collectClass
    def __init__(self):
        pass

    @d6tcollect._collectClass
    def somefct(self):
        print('hello world')

@d6tcollect.collect
def somefct(a,b):
    return a+b

