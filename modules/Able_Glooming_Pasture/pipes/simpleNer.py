#!/usr/bin/env python
import nltk

from nltk import word_tokenize,pos_tag,ne_chunk

import sys
import re

PStemmer = nltk.PorterStemmer()

#####################################################
if __name__ == '__main__':

    line = 'init'
    while line != '':
        line = sys.stdin.readline()
        if line != '':
            line = re.sub(r'a','e',line)
            sys.stdout.write(line)
        else:
            pass
