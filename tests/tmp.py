
import importlib


import d6tcollect
d6tcollect.submit = True
d6tcollect.ignore_errors = False
d6tcollect.host = 'http://192.168.33.10:5000'
d6tcollect.host = 'https://d6tpipe-staging-demo.herokuapp.com'
d6tcollect.host = 'http://localhost:8080'

import d6tcollect.track
htmltext = '''
<html>
<body>
Hello world!
</body>
</html>
'''

import datetime
cfg_track = {
    "userid": "master@deepmind.com",
    "username": "master@deepmind.com",
    "appid": "app1",
    "appversion": "2020-01-01",
    "target": "{eventid}",
}

tracker = d6tcollect.track.TrackAppUserEmail(htmltext,cfg_track['appid'],cfg_track['target'])
r = tracker.process_all(['a@b.com','c@d.com'])

quit()
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

