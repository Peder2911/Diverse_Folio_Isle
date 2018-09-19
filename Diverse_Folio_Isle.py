import sys
import os
import logging

mypath = os.path.dirname(os.path.abspath(__file__))
sys.path.append(mypath)

from lib.Director import Director

class Session():
    def __init__(self,scriptfolder):
        self.Director = Director()
        self.scriptfolder = os.path.join(mypath,scriptfolder)
    def run(self):
        self.Director.lineup(self.scriptfolder)

if __name__ == '__main__':
    logging.basicConfig(level = 1)
    Sess = Session('scripts')
    Sess.run()

