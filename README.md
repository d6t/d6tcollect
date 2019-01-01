# d6tcollect

### Collects anonymous usage statistics for python libraries

Much like websites, this library collects anonymous usage statistics.

It ONLY collects import and function call events. It does NOT collect any of your data.

Example: `{'profile': 'prod', 'package': 'd6tmodule', 'module': 'd6tmodule.utils', 'classModule': 'd6tmodule.utils.MyClass', 'class': 'MyClass', 'function': 'MyClass0.myfunction_1', 'functionModule': 'd6tmodule.utils.MyClass.myfunction_1', 'event': 'call', 'params': {'args': 1, 'kwargs': 'another'}}`

See [privacy notice](https://www.databolt.tech/index-terms.html#privacy)
