
import os
import subprocess
from modules.myCli import myCli

import re
import fnmatch

import csv
from io import StringIO
import json

import logging

#####################################

class PipeError(Exception):
    pass

class FileError(Exception):
    pass

#####################################

cl = logging.getLogger('base_console')

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

def stringToStdFormat(string):
    fauxFile = StringIO(string)

    with fauxFile as csvFile:
        reader = csv.reader(csvFile)
        names = next(reader)

        result = []
        for line in reader:

            lineResult = {}
            for n,entry in enumerate(line):
                lineResult.update({names[n]:entry})

            result.append(lineResult)

    return(result)

#####################################
# Sourcing functions
def constructCsvDat():
    dataFile = input('Please enter datafile\n~ ')

    def csvDat(dataFile = dataFile):
        with open(dataFile) as file:
            data = file.read()
        return(data.encode())

    return(csvDat)

#####################################
def constructDbDat():
    dbFile = input('Please enter dbFile\n~ ')
    id = input('Please enter ID (leave empty for all)\n~ ')
    dbFile = os.path.abspath(dbFile)

    arguments = [dbFile]
    if id != '':
        arguments += [id]

    def dbDat(dbFile = dbFile,id = id,arguments = arguments):
        sqliteQuery_r = pipeProcess('rscript',
                                    './modules/Pattern/sqliteQuery.r',
                                    arguments = arguments)
        return(sqliteQuery_r.stdout)

    return(dbDat)

#####################################
def constructQueryDat():
    source = myCli.menu(['nyt','guardian'],prompt='Please select source')
    query = input('Please enter query\n~ ')

    loc,startYr,endYr = query.split('_')

    args = [source,startYr,endYr]
    if source == 'nyt':
        args += ['glocations.contains',loc]
    else:
        args += [loc]

    def queryDat(args = args):
        getArticles_py = pipeProcess('python',
                                     './modules/Montanus/getArticles.py',
                                     arguments = args)
        jsonToCsv_r = pipeProcess('rscript',
                                  './modules/Pattern/jsonToCsv.r',
                                  input = getArticles_py.stdout)

        return(jsonToCsv_r.stdout)

    return(queryDat)

#####################################
# Analysis functions
def constructClassVecs():

    s2v = os.path.abspath('./modules/sent2vec/fasttext')
    vectorizer = myCli.fileMenu('resources/models/embedders',
                                prompt = 'Select vectorizer model',
                                filetype = 'bin')
    classifier = myCli.fileMenu('resources/models/classifiers',
                                prompt = 'Select classifier model',
                                filetype = 'rds')

    def classVecs(data,
                  s2v = s2v,
                  vectorizer = vectorizer,
                  classifier = classifier):

        classify_r = pipeProcess('rscript',
                                 './modules/Pattern/classify.r',
                                 [s2v,vectorizer,classifier],
                                 input = data)

        outData = classify_r.stdout.decode()

        return(outData)

    return(classVecs)

#####################################
def constructClusterVecs():

    tracerFile = input('\nPlease provide a tracer-file:\n~ ')
    s2v = os.path.abspath('./modules/sent2vec/fasttext')
    vectorizer = myCli.fileMenu('resources/models/embedders',
                                prompt = 'Select vectorizer model',
                                filetype = 'bin')

    def clusterVecs(data,
                    s2v = s2v,
                    vectorizer = vectorizer,
                    tracerFile = tracerFile):

        cluster_r = pipeProcess('rscript',
                                './modules/Pattern/clusterPipe.r',
                                [tracerFile,s2v,vectorizer],
                                input = data)

        outData = cluster_r.stdout.decode()

        return(outData)

    return(clusterVecs)

def constructPatternSearch():

    def fnSearch(data,pattern):
        data = data.split(' ')

        match = False
        for w in data:
            match |= fnmatch.fnmatch(w,pattern)

        return(match)

    def search(data,field,engine,pattern):

        patternOrsAnds = [pat.split('and') for pat in pattern.split('or')]

        result = []
        for entry in data:
            match = False

            orMatch = []
            for orClause in patternOrsAnds:

                andMatch = []
                for andClause in orClause:

                    pattern = andClause.strip()
                    if engine == 'regex':
                        andMatch.append(re.search(pattern,entry[field]))
                    elif engine == 'glob':
                        andMatch.append(fnSearch(entry[field],pattern))
                    else:
                        pass

                orMatch.append(all(andMatch))

            match = any(orMatch)

            if match:
                result.append(entry)

        return(result)

    field = myCli.menu(['body','headline'],prompt = 'Select field to search:')
    engine = myCli.menu(['regex','glob'],prompt = 'Select search engine:')
    pattern = input('\nEnter search pattern (%s):\n'%(engine))

    def patternSearch(data,field = field,engine = engine,pattern = pattern):
        data = stringToStdFormat(data.decode())

        with open('testResources/testjson.json','w') as jFile:
            json.dump(data,jFile)

        data = search(data,field,engine,pattern)
        data = json.dumps(data)+'\n'

        jsonToCsv_r = pipeProcess('rscript',
                                  './modules/Pattern/jsonToCsv.r',
                                  input = data.encode())

        result = jsonToCsv_r.stdout.decode()
        return(result)

    return(patternSearch)

#####################################
# Treatment functions
def constructAgpTreat():

    def agpProcess(data,command):
        data = pipeProcess('python',
                           './modules/Able_Glooming_Pasture/abGloPa.py',
                           [command],
                           input=data)
        return(data)

    options = input('Options for AGP:\n~')
    options = options.split(' ')

    def agpTreat(data):
        if '-c' in options or '--clean' in options:
            data = agpProcess(data,'clean')
        if '-n' in options or '--ner' in options:
            data = agpProcess(data,'ner')
        if '-s' in options or '--stem' in options:
            data = agpProcess(data,'stem')
        if '-n' in options or '--normalize' in options:
            data = agpProcess(data,'normalize')

        return(data)

    return(agpTreat)

#####################################
