# d6tcollect

### Collects anonymous usage statistics for python libraries

Much like websites, this library collects anonymous usage statistics.

It ONLY collects import and function call events. It does NOT collect any of your data.

Example of data collected `{'package': 'module', 'module': 'module.utils', 'classModule': 'module.utils.MyClass', 'class': 'MyClass', 'function': 'MyClass0.myfunction_1', 'functionModule': 'module.utils.MyClass.myfunction_1', 'event': 'call', 'params': {'args': 1, 'kwargs': 'another'}}`

See [privacy notice](https://www.databolt.tech/index-terms.html#privacy)

To disable collection run the blow before importing libraries which use d6tcollect

```python

import d6tcollect
d6tcollect.submit = False
```
