# memcached-search

A simple tool for finding keys and values in a memcached server or cluster. Especailly good for locating values in WordPress's object cache when you do not know the cache key.

<p align="center">
<a href="http://10up.com/contact/"><img src="https://10updotcom-wpengine.s3.amazonaws.com/uploads/2016/10/10up-Github-Banner.png" width="850"></a>
</p>

## Installing

Install from pip:

```Shell
pip install memcached-search
```

## Requirements

Supports Python 2 and 3 (tested on 2.7.15 and 3.6). Requires the following packages:

```Shell
Click
pymemcache
future
future-fstrings
```

## Usage

```Shell
Usage: memcached-search [OPTIONS] COMMAND [ARGS]...

  Debug your memcached server by searching for cache keys

Options:
  --host TEXT     memcached server ip
  --port INTEGER  memcached port
  --help          Show this message and exit.

Commands:
  find   search for cache keys matching a regex...
  get    Get value from cache by cache key
  items  List all items in memcached server
```

## Configuration

By default, memcached-search connects to memcached runnging on localhost, on the default port of 11211. This can be customized by creating a JSON formatted config file in the current users home directory: `~/.memcached-search`. This file should contain a JSON array whos elements are arrays of server and port combonations for each server to connect to.

```JSON
[
    ["localhost", 11211],
    ["localhost", 11212]
]
```