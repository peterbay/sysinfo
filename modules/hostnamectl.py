
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r'^([^:]+):\s*(.*)', line)
            if lineMatch:
                output[camelCase(lineMatch.group(1))] = lineMatch.group(2)
    
    return {'output': output}

def register(main):
    main['hostnamectl'] = {
        'cmd': 'hostnamectl status',
        'description': 'Current system hostname and related information',
        'parser': parser
    }