import subprocess
import os

#####################################

def relPath(filePath,fileVar):
    selfPath = os.path.dirname(fileVar)
    relPath = os.path.join(selfPath,filePath)
    return(relPath)

def pipeProcess(interpreter,file,arguments=[],logger=None,**kwargs):
        script = [interpreter,file]
        script += arguments

        if not logger is None:
            logger.debug('running ' + os.path.abspath(script[1]))

        p = subprocess.run(script,
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE,
                           **kwargs)

        try:
            p.check_returncode()
        except subprocess.CalledProcessError:
            if not logger is None:
                logger.critical(p.stderr.decode())
            raise subprocess.CalledProcessError

        stderr = p.stderr.decode().strip()
        if stderr != '' and not logger is None:
            logger.debug(stderr)

        return(p)
