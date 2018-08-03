#!/usr/bin/env python
import os
import sys

import re

class FileError(Exception):
    pass


def menu(options,prompt='make a selection'):
    print(prompt)
    for number,option in enumerate(options):
        print(str(number) + ' - ' + str(option))

    selectionNo = sys.maxsize
    while not 0 <= selectionNo <= len(options):
        try:
            selectionNo = int(input('~ '))
        except ValueError:
            print('please enter a number')

    return(options[selectionNo])

def functionMenu(functions,prompt = 'select function'):
    fNames = {fun.__name__:fun for fun in functions}
    selection = menu([*fNames.keys()],prompt = prompt)
    return(fNames[selection])

def fileMenu(folder,filetype,prompt = 'select file'):
    files = os.listdir(folder)

    typeLen = len(filetype)
    files = [f for f in files if f[-typeLen:] == filetype]
    if len(files) == 0:
        raise FileError('No files of type %s in %s'%(filetype,folder))

    file = menu(files,prompt = prompt)
    path = os.path.join(folder,file)
    return(path)

if __name__ == '__main__':
    print(fileMenu(sys.argv[1],sys.argv[2]))
