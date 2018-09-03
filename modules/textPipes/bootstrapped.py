#!/usr/bin/env python
from nltk.corpus import wordnet
import sys

synonymized = []

def synonymize(sent):
    words = [w.strip() for w in sent.split(' ')]
    synsets = wordnet.synsets(words[0])
    if len(synsets) > 0:
        lemmas = synsets[0].lemmas()
        lemmas = ','.join([l.name() for l in lemmas])
        return(lemmas)
    else:
        return(str(words))

input = 'init'
while input != '': = sys.stdin.readline()
    output = synonymize(input)
    sys.stdout.write(output+'\n')
