#!/usr/bin/env python
import nltk

import sys
import re

PStemmer = nltk.PorterStemmer()

#####################################################
#FIXME
if __name__ == '__main__':

    line = 'init'
    while line != '':
        line = sys.stdin.readline()
        if line != '':
            line = re.sub(r'a','e',line)
            sys.stdout.write(line)
        else:
            pass
