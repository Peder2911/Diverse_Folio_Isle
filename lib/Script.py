import subprocess
import os
import json
import time
import logging
# Basic script class

cl = logging.getLogger('console')

class Script():

    def __init__(self,path):
        self.path = path
        self.id = os.path.join(self.path,'id.json')
        with open(self.id) as idfile:
            self.id = json.load(idfile)
        # Options are configured in Director before running
        self.options = []

    def run(self):

        executable = os.path.join(self.path,self.id['executable'])

        call = [self.id['interpreter'],executable]

        if 'args' in self.id.keys():
            args = self.id['args'].split()
            call += args
    
        cl.debug('\ncalling %s'%(' '.join(call)))


        self.p = subprocess.Popen(call,
                                  stdin = subprocess.PIPE)

        jsonOpts = json.dumps(self.id['options'])
        jsonOpts += '\n'
        jsonOpts = jsonOpts.encode()

        self.p.stdin.write(jsonOpts)
        self.p.stdin.close()

        while self.p.poll() is None:
            time.sleep(1)

        if self.p.poll() != 0:
            raise subprocess.SubprocessError('nonzero exit code for %s'%(self.path))

    def __del__(self):
        try:
            self.p.kill()
        except AttributeError:
            pass


