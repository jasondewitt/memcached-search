#!/usr/bin/env python
import click
import re
import json
import sys
import os

_key_regex = re.compile(r'ITEM (.*) \[(.*); (.*)\]')
_slab_regex = re.compile(r'items:(.*):number')
_stat_regex = re.compile(r"STAT (.*) (.*)\r")

@click.group()
@click.option("--host", help="memcached server ip", default="localhost")
@click.option("--port", help="memcached port", default=11211)
@click.pass_context
def cli(ctx, host, port):
    """Debug your memcached server by searching for cache keys"""
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj["HOST"] = host
    ctx.obj["PORT"] = port


@cli.command()
@click.pass_context
def items(ctx):
    """List all items in memcached server"""
    config = buildConfig(ctx.obj["HOST"], ctx.obj["PORT"])
    clientList = getClientList(config)
    for client in clientList:
        click.echo(f"FROM SERVER {client.server}")
        for id in slabIds(client.stats("items")):
            for key in client.stats('cachedump', id, '0').keys():
                click.echo(key)
        print()


@cli.command()
@click.argument("pattern")
@click.pass_context
def find(ctx, pattern):
    """search for cache keys matching a regex pattern"""
    config = buildConfig(ctx.obj["HOST"], ctx.obj["PORT"])
    clientList = getClientList(config)
    for client in clientList:
        click.echo(f"FROM SERVER {client.server}")
        for id in slabIds(client.stats("items")):
            for key in client.stats('cachedump', id, '0').keys():
                if re.search(pattern, key.decode('utf-8')):
                    click.echo(key)
        print()


@cli.command()
@click.argument("key")
@click.pass_context
def get(ctx, key):
    """Get value from cache by cache key"""
    config = buildConfig(ctx.obj["HOST"], ctx.obj["PORT"])
    client = getClient(config)
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
    if len(ids) == 0:
        click.echo("No slabs found, does this memcached server contain data?")
        sys.exit(1)
    return ids


def buildConfig(host, port):
    configFile = os.path.expanduser('~/.memcached-search.conf')
    if os.path.exists(configFile):
        with open(configFile, 'r') as f:
            try:
                config_list = json.load(f)
                config =[]
                for server in config_list:
                    config.append( tuple((server[0], server[1])) )
            except Exception as e:
                print("Config file is not properly formatted\n")
                raise(e)
        return config
    else:
        return [ tuple((host, port)) ]


def getClient(config):
    if type(config) == list:
        from pymemcache.client.hash import HashClient
        return HashClient(config)
    else:
        from pymemcache.client.base import Client
        return Client(config[0])


def getClientList(config):
    from pymemcache.client.base import Client
    configList = []
    for c in config:
        configList.append(Client(c))

    return configList