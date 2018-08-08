
from nltk import tokenize

import csv
import json
import re

import os
import sys
import subprocess
from io import StringIO

def relPath(path):
    selfPath = os.path.dirname(__file__)
    relPath = os.path.join(selfPath,path)
    return(relPath)

def nlSepSentences(text):
    text = text.replace('\n',' ')
    text = tokenize.sent_tokenize(text)
    text = '\n'.join(text)
    return(text)

if __name__ == '__main__':
    '''
    Hacks to list-of-dictionaries format
    '''
    
    ff = StringIO(sys.stdin.read())
    reader = csv.reader(ff)
    names = next(reader)

    data = []
    for line in reader:

        lineResult = {}
        for n,entry in enumerate(line):
            lineResult.update({names[n]:entry})

        data.append(lineResult)

    for entry in data:
        entry['body'] = nlSepSentences(entry['body'])

    data = json.dumps(data)

    jsonToCsv_r = relPath('../jsonToCsv.r')
    jsonToCsv_r = subprocess.run(['rscript',jsonToCsv_r],
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE,
                                 input = data.encode())

    err = jsonToCsv_r.stderr.decode()
    if err != '':
        for line in err.split('\n'):
            print(line,file = sys.stderr)

    data = jsonToCsv_r.stdout.decode()
    print(data,file = sys.stdout)
