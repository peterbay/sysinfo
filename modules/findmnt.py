
from sysinfo_lib import parseTable

def parser(stdout, stderr):
    output = {}
    if stdout:
        output = parseTable(stdout)
    
    return {'output': output}

def register(main):
    main['findmnt'] = {
        'cmd': 'findmnt -Al | column -t',
        'description': 'List all mounted filesytems',
        'parser': parser
    }