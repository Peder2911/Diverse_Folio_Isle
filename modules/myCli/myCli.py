
import os
import sys

import re

class FileError(Exception):
    pass

def fileMenu(folder,prompt='select file',filetype = 'rds'):
    print(prompt)
    files = os.listdir(folder)

    typeLen = len(filetype)
    files = [f for f in files if f[-typeLen:] == filetype]
    if len(files) == 0:
        raise FileError('No files of type %s in %s'%(filetype,folder))

    for number,file in enumerate(files):
        print(str(number) + ' - ' + file)

    selectionNo = sys.maxsize

    while not 0 <= selectionNo <= len(files)-1:
        selectionNo = int(input('~ '))

    file = files[selectionNo]
    path = os.path.join(folder,file)
    return(path)

if __name__ == '__main__':
    print(fileMenu(sys.argv[1]))
