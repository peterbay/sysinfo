
from sysinfo_lib import parseTable

def parser(stdout, stderr):
    output = {}
    if stdout:
        output = parseTable(stdout)
    
    return {'output': output}

def register(main):
    main['busctl'] = {
        'cmd': 'busctl --no-pager | column -t',
        'description': 'Introspect the bus',
        'parser': parser
    }
