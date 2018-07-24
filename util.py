#!/usr/bin/env python

from modules.util import dbTools,dataTools
import fire
import subprocess

class functions():

    def dbFacts(self,dbFile):
        dbTools.dbFacts(dbFile)

    def populateDB(self,source,rosterFile,dbFile):
        call = ['python','./autogrep.py',source,rosterFile,dbFile]

        try:
            subprocess.run(call)
        except SubprocessError:
            print('oh no! (subprocess error)') #TODO error handling

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
