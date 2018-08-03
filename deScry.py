#!/usr/bin/env python
import fire
import os
import subprocess

from modules.util import dbTools
from modules.myCli import myCli

from io import StringIO

#####################################

import logging

from logging.config import dictConfig

import yaml
import json
import csv

with open('resources/config/logging.yaml') as file:
    logConf = yaml.load(file)
    logConf['handlers']['file']['filename'] = 'logs/deScry.log'

dictConfig(logConf)

fl = logging.getLogger('base_file')
cl = logging.getLogger('base_console')

#####################################

class PipeError(Exception):
    pass

class FileError(Exception):
    pass

#####################################

class functions():

    print('\n'+'#'*38)
    with open('./resources/spice/banner.txt') as file:
        print(file.read())
    print('By Peder G. Landsverk 2018')
    print('Peace Research Institute Oslo')
    print('#'*38+'\n')

    def analyze(self):

        #####################################
        # Sourcing functions

        def csvDat():
            dataFile = input('Please enter datafile\n~ ')

            with open(dataFile) as file:
                data = file.read()
            return(data.encode())

        def dbDat():
            dbFile = input('Please enter dbFile\n~ ')
            id = input('Please enter ID (* for all)\n~ ')

            dbFile = os.path.abspath(dbFile)
            sqliteQuery_r = pipeProcess('rscript',
                                        './modules/Pattern/sqliteQuery.r',
                                        arguments = [dbFile,id])

            return(sqliteQuery_r.stdout)

        def queryDat():
            source = myCli.menu(['nyt','guardian'],prompt='Please select source')
            query = input('Please enter query\n~ ')

            loc,startYr,endYr = query.split('_')

            args = [source,startYr,endYr]
            if source == 'nyt':
                args += ['glocations.contains',loc]
            else:
                args += [loc]

            getArticles_py = pipeProcess('python',
                                         './modules/Montanus/getArticles.py',
                                         arguments = args)
            jsonToCsv_r = pipeProcess('rscript',
                                      './modules/Pattern/jsonToCsv.r',
                                      input = getArticles_py.stdout)

            return(jsonToCsv_r.stdout)

        #####################################
        # Analysis functions

        def classVecs(data):

            s2v = os.path.abspath('./modules/sent2vec/fasttext')

            vectorizer = myCli.fileMenu('resources/models/embedders',
                                        prompt = 'Select vectorizer model',
                                        filetype = 'bin')
            classifier = myCli.fileMenu('resources/models/classifiers',
                                        prompt = 'Select classifier model',
                                        filetype = 'rds')

            classify_r = pipeProcess('rscript',
                                     './modules/Pattern/classify.r',
                                     [s2v,vectorizer,classifier],
                                     input = data)

            outData = classify_r.stdout.decode()
            return(outData)

        def clusterVecs(data):
            tracerFile = input('Please provide a tracer-file:\n~ ')
            s2v = os.path.abspath('./modules/sent2vec/fasttext')

            vectorizer = myCli.fileMenu('resources/models/embedders',
                                        prompt = 'Select vectorizer model',
                                        filetype = 'bin')
            cluster_r = pipeProcess('rscript',
                                    './modules/Pattern/clusterPipe.r',
                                    [tracerFile,s2v,vectorizer],
                                    input = data)

            outData = cluster_r.stdout.decode()
            return(outData)

        def agpTreat():
            pass

        #####################################

        dFunction = myCli.functionMenu([csvDat,dbDat,queryDat],
                                       prompt = 'Select data source')
        anFunction = myCli.functionMenu([classVecs,clusterVecs],
                                       prompt = 'Select analysis method')

        outFile = input('Please enter outfile:\n')

        data = dFunction()
        analyzed = anFunction(data)

        cl.debug('writing data to %s'%(outFile))

        with open(outFile,'w') as file:
            file.write(analyzed)

def inputToFunction(nameSpace,choices):
    selection = ['']

    while selection[0] not in choices:
        string = input('~ ')
        selection = string.split(' ')

    selected_function = getattr(nameSpace,selection[0])
    args = selection[1:]

    return(selected_function,args)


def pipeProcess(interpreter,file,arguments=[],**kwargs):
        script = [interpreter,file]
        script += arguments

        cl.debug('running ' + os.path.abspath(script[1]))

        p = subprocess.run(script,
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE,
                           **kwargs)

        try:
            p.check_returncode()
        except subprocess.CalledProcessError:
            cl.critical(p.stderr.decode())
            fl.critical(p.stderr.decode())
            raise PipeError
        stderr = p.stderr.decode().strip()
        if stderr != '':
            cl.debug(stderr)

        return(p)

def checkFiles(*args):

    for file in args:
        if not os.path.isfile(file):
            cl.critical('Could not find file: ' + file)
            raise FileError

#####################################

if __name__=='__main__':
    fire.Fire(functions)
