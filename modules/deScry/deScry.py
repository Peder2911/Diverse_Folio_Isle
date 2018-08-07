# This class represents a deScry session
# There are three processes needed to perform data analysis:

# Sourcing : How the data is gathered
# Treatment : How the data is treated before analysis
# Analysis : How the data is analyzed

import sys
import logging

cl = logging.getLogger('base_console')
#TODO implement logging

class session():

    def __init__(self):
        # Must be set (#TODO provide defaults?)
        self.sourceFunction = None
        self.treatmentFunction = None
        self.analysisFunction = None
        self.outfile = './out'

    def run(self):
        data = self.sourceFunction()

        if self.treatmentFunction:
            data = self.treatmentFunction(data)
        else:
            pass

        if self.analysisFunction:
            results = self.analysisFunction(data)
        else:
            results = data.decode()

        if self.outfile:
            with open(self.outfile,'w') as file:
                file.write(results)

        else:
            print(results,file = sys.stdout)

    '''
    def treat(self):

        data = self.sourceFunction()
        data = self.treatmentFunction(data)

        if self.outfile:
            with open(self.outfile,'w') as file:
                file.write(data)
        else:
            print(data,file = sys.stdout)
    '''
