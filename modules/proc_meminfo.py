
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            keyValueSearch = re.search(r'^([^:]+):\s*(.*)$', line, re.IGNORECASE)
            if keyValueSearch:
                key = keyValueSearch.group(1).strip(':')
                value = keyValueSearch.group(2).strip()

                valueSearch = re.search(r'(.*)\s+(.*)$', value)
                if valueSearch:
                    output[camelCase(key)] = {
                        'value': valueSearch.group(1),
                        'type': valueSearch.group(2)
                    }
                else:
                    output[camelCase(key)] = {
                        'value': value,
                        'type': ''
                    }

    return {'output': output}

def register(main):
    main['proc_meminfo'] = {
        'cmd': 'cat /proc/meminfo',
        'description': 'Reports a large amount of valuable information about the systems RAM usage',
        'parser': parser
    }
