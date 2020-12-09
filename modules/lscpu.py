
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            line = re.sub(r'\(s\)', 's', line)
            lineMatch = re.search(r'^([^:]+):\s*(.*)', line)
            if lineMatch:
                output[camelCase(lineMatch.group(1))] = lineMatch.group(2)
    
    return {'output': output}

def register(main):
    main['lscpu'] = {
        'cmd': 'lscpu',
        'description': 'Information about the CPU architecture',
        'parser': parser
    }