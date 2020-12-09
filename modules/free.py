
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    columns = None
    if stdout:
        typeName = ''
        for line in stdout.splitlines():
            if re.search(r'total\s+used', line, re.IGNORECASE):
                columns = re.split(r'\s+', line.strip())

            entrySearch = re.search(r'^([^:]+):\s+(.*)$', line)
            if columns and entrySearch:
                type = camelCase(entrySearch.group(1))
                output[type] = {}
                for idx, value in enumerate(re.split(r'\s+', entrySearch.group(2).strip())):
                    if idx < len(columns):
                        output[type][columns[idx]] = value

    return {'output': output}

def register(main):
    main['free'] = {
        'cmd': 'free -b -l -w',
        'description': 'Amount of free and used memory in the system',
        'parser': parser
    }
