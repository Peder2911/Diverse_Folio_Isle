#!/usr/bin/env python

from modules.util import dbTools,dataTools,processHelpers
import fire
import subprocess
import sys

class functions():

    def dbFacts(self,dbFile):
        dbTools.dbFacts(dbFile)

    def populateDB(self,source,rosterFile,dbFile):

        try:            
            call = ['python','./buildDB.py',source,rosterFile,dbFile]
            processHelpers.run(call,errTo=sys.stderr)
        except subprocess.SubprocessError:
            print('oh no! (subprocess error)') #TODO error handling
            sys.exit(1)

    def getSentences(self,dbFile,outFile):
        res = dbTools.bulkGet(dbFile,'sentences','body')
        res = dataTools.bodiesToSentences(res)

        with open(outFile,'w') as file:
            for sent in res:
                file.write(sent)
                file.write('\n')

#####################################

if __name__=='__main__':
    fire.Fire(functions)
