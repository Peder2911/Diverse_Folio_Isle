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

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

cl = logging.getLogger('console')

from Cli import Cli
from myExceptions import IdError

class Director():
    def __init__(self):

        self.Cli = Cli(demarcate = True)
        self.processes = []

    def __del__(self):
        [p.kill() for p in self.processes]
    
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
        
        options = [self.configure(script,masterConfig) for script in scripts]

        for script,option in OrderedDict(zip(scripts,options)).items():
            self.runScript(script,option)

    def runScript(self,scriptpath,options):
        # Run the executable, with the interpreter, both specified in the id.json doc.
        # This function also writes options to the process, that are figured out earlier.
        
        iddoc = os.path.join(scriptpath,'id.json')
        with open(iddoc) as file:
            jload = json.load(file)
            interpreter = jload['interpreter']
            executable = os.path.join(scriptpath,jload['executable'])

        p = subprocess.Popen([interpreter,executable],
                            stdin = subprocess.PIPE)

        self.processes.append(p)
        options = json.dumps(options).encode()
        p.stdin.write(options)
        p.stdin.close()

        while p.poll() is None:
            time.sleep(1)
            cl.debug('sleeping')
        if p.poll() != 0:
            cl.critical('Something went wrong with %s'%(scriptpath))
            cl.critical('Exit code: %i'%(p.poll()))

    def configure(self,scriptpath,masterConfig):
        # Configure a script using its id.json file and the Cli

        iddoc = os.path.join(scriptpath,'id.json')
        with open(iddoc) as file:
            jload = json.load(file)
            options = jload['options']
            scriptname = jload['name']
        
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
        return(options)

if __name__ == '__main__':
    # Test suite
    # Uses the scripts/*/test script-folders to test functionality.

    logging.basicConfig(level = 0)
    cl.setLevel('DEBUG')

    tDirector = Director()
    tDirector.lineup('../scripts')
