
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {
        'processor': {},
        'hardware': {},
        'oth': {}
        }

    if stdout:
        for block in re.split(r'\r\r|\n\n|\r\n\r\n', stdout):
            sub = {}
            for line in block.splitlines():
                values = re.search(r'([^\t]+)\s*:\s*(.*)$', line)
                if values:
                    sub[camelCase(values.group(1).strip())] = values.group(2).strip()

            if 'processor' in sub:
                output['processor'][sub['processor']] = sub

            elif 'hardware' in sub:
                output['hardware'] = sub

            else:
                output['oth'] = sub

    return {'output': output}

def register(main):
    main['proc_cpuinfo'] = {
        'cmd': 'cat /proc/cpuinfo',
        'description': 'Type of processor used by your system',
        'parser': parser
    }
