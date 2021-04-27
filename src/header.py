
import urllib.request, urllib.error, urllib.parse
import sys
import os
import pymongo

def getClient():
    if 'MONGO_DB_URI' in os.environ:
        return pymongo.MongoClient(os.environ['MONGO_DB_URI'])
    else:
        return pymongo.MongoClient()

def getServerStatus():
    c = getClient()
    return c.admin.command('serverStatus', workingSet=True)
