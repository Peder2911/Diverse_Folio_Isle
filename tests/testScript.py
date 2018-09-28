import subprocess

import sys
import os
import time

import json

junkJson = '''
    {
        "spam":"eggs",
        "ham":"foo",
        "bar":"baz"
    }

'''.encode()

import logging
cl = logging.getLogger('console')

scriptpath = sys.argv[1]

if os.path.isfile(scriptpath):
    scriptpath = os.path.abspath(scriptpath)

else:
    print('no such script %s',file = sys.stderr)
    sys.exit(1)


def testScript(scriptpath):
    iddocpath = os.path.join(os.path.dirname(scriptpath),'id.json')
    with open(iddocpath) as file:
        iddict = json.load(file)

    opts = iddict['options']
    for opt in opts:
        opts[opt] = input('Enter value for %s'%(opt)) 

    with open('masterConfig.json') as file:
        mconf = json.load(file)

    opts.update(mconf)

    opts = json.dumps(opts).encode()
    
    executable = scriptpath
    interpreter = iddict['interpreter']
    print('testing %s'%(iddict['name']))

    call = [interpreter,executable,'--dfi']

    p = subprocess.Popen(call,
                         stdin = subprocess.PIPE)
    p.stdin.write(opts)
    p.stdin.close()

    while p.poll() is None:
        time.sleep(1)
    if p.poll() != 0:
        cl.critical('something went wrong!!')

testScript(scriptpath)
    

