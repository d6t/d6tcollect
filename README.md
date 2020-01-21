# d6tcollect

### What it does?

Much like websites, this library collects anonymous usage statistics for python libraries.

### Why collect?

We have put a lot of effort into making the libraries useful to you. Users typically run into problems but a lot of people don't report issues. We also don't know which features users find valuable. Without this information we wouldn't know what bugs to fix and what features to develop. We want to make the libraries better but we want to make data-driven decisions.

### What it collects?

It ONLY collects select function call events and exceptions. It does NOT collect any of your data.

Example of data collected `{'package': 'module', 'module': 'module.utils', 'classModule': 'module.utils.MyClass', 'class': 'MyClass', 'function': 'MyClass0.myfunction_1', 'functionModule': 'module.utils.MyClass.myfunction_1', 'event': 'call', 'params': {'args': 1, 'kwargs': 'another'}}`

Data transfer is minimal and run asynchronous so it doesn't impact your code in any way.

If you don't trust our word, just look at the code!

### How to disable?

To disable collection run the below before importing libraries which use d6tcollect

```python

import d6tcollect
d6tcollect.submit = False
```

### Privacy Notice

See https://www.databolt.tech/index-terms.html#privacy

## Email engagement tracking

With a d6tcollect server you can track email engagement ie read receipts and link clicks. Allows for on-prem internal deployment.
[Request demo](https://pipe.databolt.tech/gui/request-premium/)
