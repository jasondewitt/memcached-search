#!/usr/bin/env python
from pymemcache.client.base import Client
import click
import re

_key_regex = re.compile(r'ITEM (.*) \[(.*); (.*)\]')
_slab_regex = re.compile(r'items:(.*):number')
_stat_regex = re.compile(r"STAT (.*) (.*)\r")

@click.group()
def cli():
    """Debug your memcached server by searching for cache keys"""

    #pass

@cli.command()
def items():
    """List all items in memcached server"""
    for id in slabIds(client.stats("items")):
        for key in client.stats('cachedump', id, '0').keys():
            click.echo(key)

    #print(_slab_regex.findall(client.stats('items')))

@cli.command()
@click.argument("pattern")
def find(pattern):
    """search for cache keys matching a regex pattern"""
    for id in slabIds(client.stats("items")):
        for key in client.stats('cachedump', id, '0').keys():
            if re.search(pattern, key.decode('utf-8')):
                click.echo(key)
        
@cli.command()
@click.argument("key")
def get(key):
    """Get value from cache by cache key"""
    click.echo(client.get(key))


def slabIds(items):
    # accepts dict of item stats
    # returns list of slabids
    ids = []
    for key in items.keys():
        try:
            m = _slab_regex.search(key.decode('utf-8'))
            found = m.group(1)
            if found not in ids:
                ids.append(found)
        except:
            pass
    return ids

def initMemcachedClient():
    return Client(('localhost', 11211))

client = initMemcachedClient()