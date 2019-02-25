'''

Much like websites, this library collects anonymous usage statistics.
It ONLY collects import and function call events. It does NOT collect any of your data.
Example: {'profile': 'prod', 'package': 'd6tmodule', 'module': 'd6tmodule.utils', 'classModule': 'd6tmodule.utils.MyClass', 'class': 'MyClass', 'function': 'MyClass0.myfunction_1', 'functionModule': 'd6tmodule.utils.MyClass.myfunction_1', 'event': 'call', 'params': {'args': 1, 'kwargs': 'another'}}
For privacy notice see https://www.databolt.tech/index-terms.html#privacy

'''

import urllib.request

import json
import threading
import uuid


submit = True
ignore_errors = True
profile = 'prod'
host = 'https://pipe.databolt.tech'
endpoint = '/v1/api/collect/'
source = 'd6tcollect'


def _request(payload):
    try:
        payload['uuid']=str(uuid.UUID(int=uuid.getnode())).split('-')[-1]
        req = urllib.request.Request(host + endpoint, data=json.dumps(payload, default=str).encode('utf-8'), headers={'content-type': 'application/json', "Source": source})
        urllib.request.urlopen(req)
    except Exception as e:
        if ignore_errors:
            pass
        else:
            raise e

def _submit(payload):
    _t = threading.Thread(target=_request, args=(payload,))
    _t.daemon = True
    _t.start()

def init(_module):

    module = _module.split('.')
    payload = {
        'profile': profile,
        'package': module[0] if len(module) > 0 else module,
        'module': _module,
        'event': 'import',
    }
    _submit(payload)

def collect(func):
    def wrapper(*args, **kwargs):
        if submit==False:
            return func(*args, **kwargs)

        module = func.__module__.split('.')
        payload = {
            'profile': profile,
            'package': module[0] if len(module)>0 else module,
            'module': func.__module__,
            'classModule': None,
            'class': None,
            'function': func.__qualname__,
            'functionModule': ".".join([func.__module__ , func.__qualname__]),
            'event': 'call',
            'params': {'args':len(args), 'kwargs':",".join(kwargs)}
        }
        _submit(payload)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            payload['event'] = 'exception'
            payload['exceptionType'] = e.__class__.__name__
            payload['exceptionMsg'] = str(e)
            _submit(payload)
            raise e

    return wrapper


def _collectClass(func):
    def wrapper(self, *args, **kwargs):
        if submit==False:
            return func(self, *args, **kwargs)

        module = func.__module__.split('.')
        payload = {
            'profile': profile,
            'package': module[0] if len(module)>0 else module,
            'module': self.__module__,
            'classModule': ".".join([self.__module__, self.__class__.__qualname__]),
            'class': self.__class__.__qualname__,
            'function': func.__qualname__,
            'functionModule': ".".join([self.__module__ , self.__class__.__name__, func.__name__]),
            'event': 'call',
            'params': {'args':len(args), 'kwargs':",".join(kwargs)}
        }
        _submit(payload)
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            payload['event'] = 'exception'
            payload['exceptionType'] = e.__class__.__name__
            payload['exceptionMsg'] = str(e)
            _submit(payload)
            raise e

    return wrapper

class Collect(type):
    def __new__(cls, name, bases, namespace, **kwds):
        namespace = {k: v if k.startswith('_') else _collectClass(v) for k, v in namespace.items()}
        return type.__new__(cls, name, bases, namespace)

