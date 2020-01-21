import youmodule

d={"profile": "dev", "class": "Collect", "function": "MyClass.myfunction_3", "module": "MyClass", "event": "call", "params": {"args": 1, "kwargs": ""}}
# d6tmodule.collect._submit(d)
# quit()

# importlib.reload(d6tmodule.run)
# import d6tcollect
# importlib.reload(d6tcollect)

# youmodule.utils.MyClass1().somefct()


myinstance = youmodule.utils.MyClass(1, 2, value=100)
print(myinstance.myfunction_1(5, another=2))
print(myinstance.myfunction_2(5))
try:
    print(myinstance.myfunction_3(2))
except:
    pass

youmodule.utils.somefct(1,1)
# youmodule.utils.somefct()

import time
print('sleep');time.sleep(10);
quit()

