
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r'^([^=]+)=(.*)$', line)
            if lineMatch:
                output[lineMatch.group(1)] = lineMatch.group(2)
    
    return {'output': output}

def register(main):
    main['env'] = {
        'cmd': 'env',
        'description': 'Environment variables',
        'parser': parser
    }