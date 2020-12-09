
from sysinfo_lib import parseTable

def parser(stdout, stderr):
    output = {}
    if stdout:
        output = parseTable(stdout)

    return {'output': output}

def register(main):
    main['blockdev'] = {
        'cmd': 'blockdev --report | column -t',
        'description': 'Block device ioctls',
        'parser': parser
    }