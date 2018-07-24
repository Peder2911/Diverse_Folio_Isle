import fire
import sys
import subprocess
import os

path = os.path.dirname(__file__) + '/tt.r'

def execute(s2vPath,modelPath,tt=False):
    p = subprocess.run(['rscript',path,s2vPath,modelPath],
                       input = sys.stdin.read().encode(),
                       stdout = subprocess.PIPE)
    sys.stdout.write(p.stdout.decode())

#####################################

fire.Fire(execute)
