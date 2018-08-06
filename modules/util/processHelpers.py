import sys
import subprocess

def run(cmd,errTo = sys.stderr,**kwargs):
    p = subprocess.Popen(cmd,stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             **kwargs)
    while p.poll() is None:
        for line in p.stderr:
            print(line.decode(),end='',file = errTo)
            errTo.flush()

    cp = {'out':p.stdout.read().decode(),
          'code':p.poll()}

    return(cp)

def errReport(message):
    print(message,file=sys.stderr)
    sys.stderr.flush()