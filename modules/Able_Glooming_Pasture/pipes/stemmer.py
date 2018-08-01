#!/usr/bin/env python
import nltk

import sys

PStemmer = nltk.PorterStemmer()

#####################################################

if __name__ == '__main__':

    line = 'init'
    while line != '':
        line = sys.stdin.readline()
        if line != '':
            words = [word.strip() for word in line.split(' ')]
            words = [PStemmer.stem(word) for word in words]

            outLine = ' '.join(words) + '\n'
            sys.stdout.write(outLine)
        else:
            pass
