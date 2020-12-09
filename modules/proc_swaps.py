
from sysinfo_lib import parseSpaceTable

def parser(stdout, stderr):
    output = {}
    if stdout:
        output = parseSpaceTable(stdout)

    return {'output': output}

def register(main):
    main['proc_swaps'] = {
        'cmd': 'cat /proc/swaps',
        'description': 'Measures swap space and its utilization',
        'parser': parser
    }