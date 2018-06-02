#!/usr/bin/env python

"""
test script to fill up your test memcached servers with random data
also requires the codename module
pip install codename
"""

from pymemcache.client.base import Client
import click
from codename import codename
import uuid
import os
import json


#client = Client(('localhost', 11211))
#client.set('some_key', 'some_value')
#result = client.get('some_key')
#print(result)

@click.command()
@click.argument('count')
@click.option("--host", help="memcached server ip", default="localhost")
@click.option("--port", help="memcached port", default=11211)
def fill(count, host, port):
    print(f"Lets fill up this memcache server with {count} keys")
    config = buildConfig(host, port)
    client = getClient(config)
    for x in range(0, int(count)):
        name = codename().replace(' ', '-')
        value = uuid.uuid4().hex
        print(f'{x} {name} {value}')
        client.set(name, value)


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

if __name__ == "__main__":
    fill()