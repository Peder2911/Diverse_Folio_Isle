# A basic Cli, including several menus, a logical (boolean) prompt (y/n), and a text prompt.
# Useful for standardization.

import os
import sys
import logging

cl = logging.getLogger('console')

class Cli():
    def __init__(self,demarcate = False,nlpad = False):
        self.demarcate = demarcate
        self.nlpad = nlpad
    
    def present(self,prompt,demarcate,nlpad):
        # Present the prompt with a demarcation line, or newline-padding?

        if nlpad:
            print()
        if demarcate:
            print('#'*38)
        
        print(prompt)


    def menu(self,options,prompt = 'make a selection'):
        # Menu that presents options of arbitrary type, ordered by number.

        choice = sys.maxsize
        while int(choice) not in range(len(options)):

            self.present(prompt,self.demarcate,self.nlpad)
            for n,option in enumerate(options):
                print(') - '.join([str(n),option]))

            try:
                choice = int(input('\n~ '))
            except ValueError:
                print('Please enter a number')

        return(options[choice])

    def filemenu(self,folder,prompt = 'select a file',menutype = 'file'):
        # Wrapper for menu, presenting choice in files or folders.

        # hide hidden files
        files = [f for f in os.listdir(folder) if f[0] != '.']

        if len(files) == 0:
            raise FileNotFoundError('No %s(s) in %s'%(menutype,folder))

        paths = [os.path.join(folder,f) for f in files]

        # only files or folders
        if menutype == 'file':
            paths = [p for p in paths if os.path.isfile(p)]
        elif menutype == 'folder':
            paths = [p for p in paths if os.path.isdir(p)]

        lookup = dict(zip(files,paths))

        choice = self.menu(files,prompt = prompt)
        fpath = lookup[choice]
        return(fpath)

    def freetext(self,prompt = 'enter text'):
        # Basic text-prompt, included for standardization reasons.

        self.present(prompt,self.demarcate,self.nlpad)
        return(input('\n~ '))

    def boolean(self,prompt = 'do you want this? (y/n)'):
        # Boolean choice (y/n)

        choice = ''
        while choice not in ['y','n']:
            self.present(prompt,self.demarcate,self.nlpad)
            choice = input('\n~ ').lower()
        return(choice == 'y')

if __name__ == '__main__':
    # Test suite

    tCli = Cli(demarcate = True,nlpad = True)

    choice = tCli.menu(['this','or','that'],prompt = 'This or that?')
    print('You chose {}'.format(choice))

    choice = tCli.filemenu('.','choose a file!')
    print('You chose {}'.format(choice))
    with open(choice) as file:
        flength = len(file.read())
        print('file contains {} characters'.format(flength))

    choice = tCli.freetext('Enter some text...')
    print('You entered {}'.format(choice))

    choice = tCli.boolean('Eggs? (y/n)')
    if choice:
        print('Eggs then')
    else:
        print('No eggs!')
