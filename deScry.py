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
    print('Peace Research Institute of Oslo')
    print('#'*38+'\n')

    def analyze(self):
        print('Select data source:')
        print('csv -dataFile')
        print('query -source -\"query\"')
        print('dbDat -dbFile -id')
        dFunction,dFunctionArgs = inputToFunction(self,
                                                  ['csvDat','query','dbDat'])

        print('Select analysis method:')
        print('classVecs -vectorizer -classifier -outFile')
        anFunction,anFunctionArgs = inputToFunction(self,
                                                    ['classVecs'])
        outFile = anFunctionArgs.pop()

        data = dFunction(*dFunctionArgs)
        analyzed = anFunction(data).stdout.decode()

        cl.debug('writing data to %s'%(outFile))
        with open(outFile,'w') as file:
            file.write(analyzed)

    #####################################
    # Sourcing functions

    def csvDat(self,dataFile):
        with open(dataFile) as file:
            data = file.read()
        return(data.encode())

    def dbDat(self,dbFile,id):
        dbFile = os.path.abspath(dbFile)
        sqliteQuery_r = pipeProcess('rscript',
                                    './modules/Pattern/sqliteQuery.r',
                                    arguments = [dbFile,id])
        return(sqliteQuery_r.stdout)


    #####################################
    # Analysis functions

    def classVecs(self,data):

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

        prepDat_r = prepDat(classify_r.stdout)
        return(prepDat_r)

    #####################################
    # Deprecated functions

    def csv(self,dataFile,mod_e,mod_c,outFile):

        with open(dataFile) as file:
            data = file.read()
        data = data.encode()

        s2v = os.path.abspath('./modules/sent2vec/fasttext')
        mod_e,mod_c,outFile = (os.path.abspath(p) for p in [mod_e,mod_c,outFile])

        #####################################

        classify_r = classify(data,s2v,mod_e,mod_c)
        prepDat_r = prepDat(classify_r.stdout)

        #####################################

        with open(outFile,'w') as file:
            file.write(prepDat_r.stdout.decode())

    def query(self,src,query,mod_e,mod_c,outFile):

        fl.debug('running %s'%(query))
        startYr,endYr,loc = query.split(' ')

        s2v = os.path.abspath('./modules/sent2vec/fasttext')
        mod_e,mod_c,outFile = (os.path.abspath(p) for p in [mod_e,mod_c,outFile])

        getArticles_py = ['python','./modules/Montanus/getArticles.py']
        if src == 'nyt':
            getArticles_py += [src,str(startYr),str(endYr),'glocations.contains',loc]
        elif src == 'guardian':
            getArticles_py += [src,str(startYr),str(endYr),loc]

        getArticles_py = subprocess.run(getArticles_py,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE)

        #####################################

        jsonToCsv_r = jsonToCsv(getArticles_py.stdout)
        classify_r = classify(jsonToCsv_r.stdout,s2v,mod_e,mod_c)
        prepDat_r = prepDat(classify_r.stdout)

        #####################################

        fl.debug('writing to %s'%(outFile))
        with open(outFile,'w') as file:
            file.write(prepDat_r.stdout.decode())

#        print(prepDat_r.stdout.decode())

    def db(self,dbFile,id,mod_emb,mod_cla,outFile):

        dbFile = os.path.abspath(dbFile)
        s2v = os.path.abspath('./modules/sent2vec/fasttext')
        mod_emb = os.path.abspath(mod_emb)
        mod_cla = os.path.abspath(mod_cla)

        checkFiles(dbFile,s2v,mod_emb,mod_cla)

        sqliteQuery_r = pipeProcess('rscript',
                                    './modules/Pattern/sqliteQuery.r',
                                    arguments = [dbFile,id])

        #####################################

        classify_r = pipeProcess('rscript',
                                 './modules/Pattern/classify.r',
                                 arguments = [s2v,mod_emb,mod_cla],
                                 input = sqliteQuery_r.stdout)

        prepDat_r = pipeProcess('rscript',
                                './modules/Pattern/prepDat.r',
                                input = classify_r.stdout)

        cl.debug('writing data to '+outFile)
        with open(outFile,'w') as file:
            file.write(prepDat_r.stdout.decode())

#####################################

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

'''def sqliteQuery(dbFile,id):
    sqliteQuery_r = pipeProcess('rscript',
                                './modules/Pattern/sqliteQuery.r',
                                arguments = [dbFile,id])
    return(sqliteQuery_r)'''

def classify(data,s2v,mod_e,mod_c):

    classify_r = ['rscript','./modules/Pattern/classify.r']
    classify_r += [s2v,mod_e,mod_c]
    classify_r = subprocess.run(classify_r,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                input = data)
    try:
        classify_r.check_returncode()
    except subprocess.CalledProcessError:
        cl.critical(classify_r.stderr.decode())
        raise PipeError

    fl.debug(classify_r.stderr.decode())

    return(classify_r)

def prepDat(data):
    prepDat_r = ['rscript','./modules/Pattern/prepDat.r']
    prepDat_r = subprocess.run(prepDat_r,
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE,
                                 input = data)
    try:
        prepDat_r.check_returncode()
    except subprocess.CalledProcessError:
        cl.critical(prepDat_r.stderr.decode())
        raise PipeError

    fl.debug(prepDat_r.stderr.decode())

    return(prepDat_r)

def jsonToCsv(data):
    jsonToCsv_r = ['rscript','./modules/Pattern/jsonToCsv.r']
    jsonToCsv_r = subprocess.run(jsonToCsv_r,
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE,
                                 input = data)
    try:
        jsonToCsv_r.check_returncode()
    except subprocess.CalledProcessError:
        cl.critical(jsonToCsv_r.stderr.decode())
        raise PipeError

    fl.debug(jsonToCsv_r.stderr.decode())

    return(jsonToCsv_r)

#####################################

if __name__=='__main__':
    fire.Fire(functions)
