import sys
import os
import logging

import json

import redis

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

from lib.Director import Director

class Session():
    def __init__(self,scriptfolder,masterConfig):
        self.Director = Director()
        self.scriptfolder = os.path.join(mypath,scriptfolder)
        self.masterConfig = masterConfig

        rconf = self.masterConfig['redis']
        self.Redis = redis.Redis(host = rconf['hostname'],
                             port = rconf['port'],
                             db = rconf['db'])

        self.checkRedis(self.Redis)
        self.Redis.delete(rconf['listkey'])

    def checkRedis(self,r):
        if r.ping():
            print('Found Redis!')
        else:
            print('Redis ping failed')
            raise Exception

    def run(self):
        self.Director.lineup(self.scriptfolder,self.masterConfig)

if __name__ == '__main__':
     
    logging.basicConfig(level = 1)
    cl = logging.getLogger('console')

    cfpath = os.path.join(mypath,'masterConfig.json')
    with open(cfpath) as cfile:
        masterConfig = json.load(cfile)

    Sess = Session('scripts',masterConfig)
    Sess.run()


