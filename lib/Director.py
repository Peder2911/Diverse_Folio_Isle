# The "director", which is basically a Cli implementation that allows you to select and
# configure the three stage-scripts before launching.
# Scripts are stored in the ./scripts/* folders as folders, containing an id.json doc that
# specifies which options to request "filled out" by this script, what interpreter to use,
# and which executable file to execute.

import sys
import os
import time

import json
import subprocess
import logging
from collections import OrderedDict

from dfitools import RedisFile

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

cl = logging.getLogger('console')

from . import Cli
from . import Script

from myExceptions import IdError

class Director():
    def __init__(self):
        self.Cli = Cli.Cli(demarcate = True)
    
    def lineup(self,scriptfolder,masterConfig):
        # Select which scripts to execute by folder, and configures their options.
        # Uses several Cli things.

        scriptfolder = os.path.join(mypath,scriptfolder)

        scripts = [
                self.Cli.filemenu(os.path.join(scriptfolder,'sourcing'),
                                    prompt = 'Select sourcing script',
                                    menutype = 'folder'),
                self.Cli.filemenu(os.path.join(scriptfolder,'preprocessing'),
                                    prompt = 'Select preprocessing script',
                                    menutype = 'folder'),
                self.Cli.filemenu(os.path.join(scriptfolder,'classification'),
                                    prompt = 'Select classification script',
                                    menutype = 'folder')
                ]

        scripts = [Script.Script(pth) for pth in scripts]

        # Configure scripts
        [self.configure(script,masterConfig) for script in scripts]

        # This is where the magic happens
        [script.run() for script in scripts]

        # And then dump the data (change this)
        f = RedisFile.RedisFile(listkey = 'data')
        with open('tmp.csv','w') as file:
            f.dump(file) 

    def configure(self,script,masterConfig):

        # Configure a script using its id.json file and the Cli

        options = script.id['options']
        scriptname = script.id['name']

        def handle(option,handler,arg = None):
            # Determine which type of CLI to use for option.
            print('\n# ' + scriptname + ' ' + '#'*(35-len(scriptname)))
            if handler == 'freetext':
                sel = self.Cli.freetext('Enter %s'%(option))
            elif handler == 'boolean':
                sel = self.Cli.boolean('%s?'%(option))
            elif handler == 'listmenu':
                options = arg.split(',')
                sel = self.Cli.menu(options,'Select %s'%(option))
            elif handler == 'filemenu':
                if os.path.isdir(arg):
                    sel = self.Cli.filemenu(arg,'Select %s from %s'%(option,arg))
                else:
                    raise IdError('Dir not found when handling %s: %s'%(option,arg))
            else:
                raise IdError('Misspecified handler for %s: %s'%(option,handler))
            return(sel)

        for option,value in options.items():
            valuelist = value.split()
            handler = valuelist[0]

            if len(valuelist) > 1:
                arg = valuelist[1]
                options[option] = handle(option,handler,arg=arg)
            else:
                options[option] = handle(option,handler)

        options.update(masterConfig)
        script.id['options'] = options

if __name__ == '__main__':
    # Test suite
    # Uses the scripts/*/test script-folders to test functionality.

    logging.basicConfig(level = 0)
    cl.setLevel('DEBUG')

    tDirector = Director()
    tDirector.lineup('../scripts')
