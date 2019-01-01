from setuptools import setup

setup(
    name='d6tcollect',
    version='1.0.1',
    packages=['d6tcollect'],
    url='https://github.com/d6t/d6tcollect',
    license='MIT',
    author='DataBolt Team',
    author_email='support@databolt.tech',
    description='d6tcollect: collects anonymous usage statistics for python libraries',
    long_description='Much like websites, this library collects anonymous usage statistics.'
        'It ONLY collects import and function call events. It does NOT collect any of your data.'
        "Example: `{'profile': 'prod', 'package': 'd6tmodule', 'module': 'd6tmodule.utils', 'classModule': 'd6tmodule.utils.MyClass', 'class': 'MyClass', 'function': 'MyClass0.myfunction_1', 'functionModule': 'd6tmodule.utils.MyClass.myfunction_1', 'event': 'call', 'params': {'args': 1, 'kwargs': 'another'}}"
        "For privacy notice see https://www.databolt.tech/index-terms.html#privacy",
    install_requires=[
    ],
    include_package_data=True,
    python_requires='>=3.5',
    keywords=['d6tcollect', 'ingest csv'],
    classifiers=[]
)
