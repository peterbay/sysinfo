
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r'^(\S+)\s+(\S+)', line)
            if lineMatch:
                output[lineMatch.group(2).strip()] = lineMatch.group(1).strip()

            lineMatch = re.search(r'^\s+(\S+)$', line)
            if lineMatch:
                output[lineMatch.group(1).strip()] = ''
    
    return {'output': output}

def register(main):
    main['proc_filesystems'] = {
        'cmd': 'cat /proc/filesystems',
        'description': 'List of the file system types currently supported by the kernel',
        'parser': parser
    }