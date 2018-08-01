#!/usr/bin/env python

import fire

import subprocess
import sys

from fun import util


#####################################

import logging

from logging.config import dictConfig

import yaml
import json
import csv

logConf = util.relPath('./resources/config/logging.yaml',__file__)
with open(logConf) as file:
    logConf = yaml.load(file)
    logConf['handlers']['file']['filename'] = 'logs/Able_Glooming_Pasture.log'

dictConfig(logConf)

fl = logging.getLogger('base_file')

#####################################

class pipes():
    def clean(self):
        #FIXME
        script = util.relPath('./pipes/cleaner.py',__file__)
        p = util.pipeProcess('python',script,
                             logger = fl,input = sys.stdin.read().encode())
        sys.stdout.write(p.stdout.decode())

    def stem(self):
        script = util.relPath('./pipes/stemmer.py',__file__)
        p = util.pipeProcess('python',script,
                             logger = fl,input = sys.stdin.read().encode())
        sys.stdout.write(p.stdout.decode())

    def ner(self):
        script = util.relPath('./pipes/nerer.py',__file__)
        p = util.pipeProcess('python',script,
                             logger = fl,input = sys.stdin.read().encode())
        sys.stdout.write(p.stdout.decode())

    def synonyms(self):
        #FIXME
        pass


#####################################

if __name__ == '__main__':
    fire.Fire(pipes)
