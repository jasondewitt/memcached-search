import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='memcached_search',
    version='0.1',
    author="Jason DeWitt",
    author_email="jason.dewitt@10up.com",
    description="A simple tools for finding keys/values in a memcached server or cluster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'Click',
        'pymemcache',
        'future',
        'future-fstrings'
    ],
    entry_points='''
        [console_scripts]
        memcached-search=memcached_search.main:cli
    ''',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)