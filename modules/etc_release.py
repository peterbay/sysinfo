
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            values = re.search(r'^([^=]+)=(.*)$', line)
            if values:
                output[values.group(1)] = values.group(2).strip().strip('"')

    return {'output': output}

def register(main):
    main['etc_release'] = {
        'cmd': 'cat /etc/*release',
        'description': 'OS release info',
        'parser': parser
    }
