
import json
import os
import logging
import sys

cl = logging.getLogger('console')
mypath = os.path.dirname(os.path.abspath(__file__))
config = json.load(sys.stdin)

for key,value in config.items():
    print(' - '.join([str(key),str(value)]))
