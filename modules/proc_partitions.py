
from sysinfo_lib import parseSpaceTable, tableToDict

def parser(stdout, stderr):
    output = {}
    if stdout:
        output = parseSpaceTable(stdout)
        output = tableToDict(output, 'name')

    return {'output': output}

def register(main):
    main['proc_partitions'] = {
        'cmd': 'cat /proc/partitions',
        'description': 'Partition block allocation information',
        'parser': parser
    }