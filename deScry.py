#!/usr/bin/env python
import fire
import os
import sys
import subprocess

from modules.util import dbTools
from modules.myCli import myCli
from modules.deScry import deScry
from dsFunctions import *

import logging
from logging.config import dictConfig

import yaml
import json
import csv

#####################################

with open('resources/config/logging.yaml') as file:
    logConf = yaml.load(file)
    logConf['handlers']['file']['filename'] = 'logs/deScry.log'

dictConfig(logConf)

cl = logging.getLogger('base_console')

#####################################

class main():

    def __init__(self):
        print('\n'+'#'*38)
        with open('./resources/spice/banner.txt') as file:
            print(file.read())
        print('By Peder G. Landsverk 2018')
        print('Peace Research Institute Oslo')
        print('#'*38+'\n')

    def analyze(self,r = False):

        session = deScry.session()

        # Chose constructors to allow for pre-selection of parameters
        ##################

        sourceOptions = [constructCsvDat,
                         constructDbDat,
                         constructQueryDat]

        sourceSelection = myCli.functionMenu(sourceOptions,
                                             prompt = 'Select data source',
                                             zeroOption = False)
        session.sourceFunction = sourceSelection()

        ##################

        #!
        def constructNlSep():
            pass
            def nlSep(data):
                call = ['python','./modules/pattern/pipes/toNlsep.py']
                p = subprocess.run(call,
                                   stdout = subprocess.PIPE,
                                   stderr = subprocess.PIPE,
                                   input = data)
                err = p.stderr.decode()

                if err != '':
                    for line in err.split('\n'):
                        cl.warning(line)

                with open('testResources/foo.txt','w') as file:
                    file.write(p.stdout.decode())

                return(p.stdout)
            return(nlSep)

        #!

        treatmentOptions = [constructAgpTreat,constructNlSep]

        treatmentSelection = myCli.functionMenu(treatmentOptions,
                                                prompt = 'Select data pre-treatment')
        session.treatmentFunction = treatmentSelection()

        ##################

        analysisOptions = [constructClassVecs,
                           constructClusterVecs,
                           constructPatternSearch]

        analysisSelection = myCli.functionMenu(analysisOptions,
                                               prompt = 'Select analysis method')
        session.analysisFunction = analysisSelection()

        ##################

        session.outfile = input('\nPlease enter outfile:\n')

        session.run()

        if r:
            self.analyze()

#####################################

if __name__=='__main__':
    fire.Fire(main)
