
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
    '''
    Converts a csv. formatted string into the list-of-dictionaries format
    used by Diverse_Folio_Isle and Able_Glooming_Pasture
    '''

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

def jsonToCsv(jsonString):
    try:
        jsonString = jsonString.encode()
        jsonString += b'\n'
    except AttributeError: #catch if not dumped
        jsonString = json.dumps(jsonString)
        jsonToCsv(jsonString)

    jsonToCsv_r = pipeProcess('rscript',
                              './modules/Pattern/jsonToCsv.r',
                              input = jsonString)
    return(jsonToCsv_r.stdout.decode())

#####################################
# Sourcing functions
'''
These functions return .csv data in bytes
'''

def constructCsvDat():
    dataFile = input('Please enter datafile\n~ ')
    std = {'headline','body','source','date','id'}

    def validateCsv(data):
        '''
        Checks if csv has required columns.
        If not, adds required columns with empty fields and complains.
        '''
        stdRow = {n:'' for n in std}

        def validateRow(row):
            columns = set(row.keys())
            val = std == columns
            missing = std - columns
            if missing == std:
                val = None
                cl.warning('%s has no valid columns'%(dataFile))
            else:
                [cl.warning('Missing %s; adding defaults'%(m)) for m in missing]
            return(val)

        def fillRow(row):
            newRow = dict(stdRow)
            for field in row:
                if field in std:
                    newRow.update({field:row[field]})
                else:
                    pass
            return(newRow)

        data = stringToStdFormat(data)
        val = validateRow(data[0])

        if val is False: # Need to fill some fields
            data = [fillRow(r) for r in data]
            #TODO add option to map std. column names to new columns
        elif val is None: # No valid fields
            data = [stdRow]

        data = jsonToCsv(json.dumps(data))

        return(data)


    def csvDat(dataFile = dataFile):
        with open(dataFile) as file:
            data = file.read()
        data = validateCsv(data)
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
# Treatment functions
'''
These functions return bytes
'''

def constructAgpTreat():
    '''
    Recieves encoded data in .csv format
    '''

    options = input('Options for AGP:\n~')
    options = options.split(' ')

    def agpTreat(data):

        data = stringToStdFormat(data.decode())
        data = json.dumps(data)

        def agpProcess(data,command):
            p = pipeProcess('python',
                            './modules/Able_Glooming_Pasture/abGloPa.py',
                            [command],
                            input=data.encode())
            return(p)

        if '-c' in options or '--clean' in options:
            p = agpProcess(data,'clean')
        if '-ne' in options or '--ner' in options:
            p = agpProcess(data,'ner')
        if '-s' in options or '--stem' in options:
            p = agpProcess(data,'stem')
        if '-no' in options or '--normalize' in options:
            p = agpProcess(data,'normalize')

        jsonToCsv_r = pipeProcess('rscript',
                                  './modules/Pattern/jsonToCsv.r',
                                  input = p.stdout)

        result = jsonToCsv_r.stdout
        return(result)

    return(agpTreat)

#####################################
# Analysis functions
'''
These functions return strings
'''

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

def constructNlSep():

    separate = 'init'
    while separate.lower() not in ['yes','y','no','n','skipnl']:
        separate = input('\nSeparate sentences? (yes/no)\n~ ')

    skip = separate in ['skipnl']
    separate = separate in ['yes','y']

    def nlSep(data):

        if not skip:
            call = ['python','./modules/Pattern/pipes/toNlsep.py']
            p = subprocess.run(call,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               input = data)
            err = p.stderr.decode()
            data = p.stdout

            if err != '':
                for line in err.split('\n'):
                    cl.warning(line)

        if separate or skip:
            call = ['rscript','./modules/Pattern/bodyToSentence.R']
            p = subprocess.run(call,
                               stdout = subprocess.PIPE,
                               stderr = subprocess.PIPE,
                               input = data)
            err = p.stderr.decode()
            data = p.stdout

            if err != '':
                for line in err.split('\n'):
                    cl.warning(line)

        return(data)
    return(nlSep)

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

        patternOrsAnds = [pat.split(' and ') for pat in pattern.split(' or ')]

        result = []
        for entry in data:
            match = False

            orMatch = []
            for orClause in patternOrsAnds:

                andMatch = []
                for andClause in orClause:

                    pattern = andClause.strip()
                    if engine == 'regex':
                        m = re.search(pattern,entry[field])
                        if m:
                            cl.debug(m.group(0))
                        andMatch.append(m)

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

#        with open('testResources/testjson.json','w') as jFile:
#            json.dump(data,jFile)

        data = search(data,field,engine,pattern)
        data = json.dumps(data)+'\n'

        jsonToCsv_r = pipeProcess('rscript',
                                  './modules/Pattern/jsonToCsv.r',
                                  input = data.encode())

        result = jsonToCsv_r.stdout.decode()
        return(result)

    return(patternSearch)
