
from sysinfo_lib import parseCharDelimitedTable, tableToDict

def parser(stdout, stderr):
    columnsNames = ['groupName', 'password', 'gid', 'groupList']
    output = parseCharDelimitedTable(stdout, ':', columnsNames)
    output = tableToDict(output, 'groupName')
    return {'output': output}

def register(main):
    main['etc_group'] = {
        'cmd': 'cat /etc/group',
        'description': 'Groups essential information',
        'parser': parser
    }

