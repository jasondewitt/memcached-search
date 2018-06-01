from setuptools import setup

setup(
    name='memcached-search',
    version='0.1',
    py_modules=['memsearch'],
    install_requires=[
        'Click',
        'pymemcache',
    ],
    entry_points='''
        [console_scripts]
        memcached-search=memsearch:cli
    ''',
)