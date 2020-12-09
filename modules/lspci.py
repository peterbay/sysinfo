
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    slot = None
    if stdout:
        for line in stdout.splitlines():
            slotSearch = re.search(r'^Slot:\s+(.*)$', line, re.IGNORECASE)
            if slotSearch:
                slot = slotSearch.group(1).strip()
                output[slot] = {}

            keyValueSearch = re.search(r'^(\S[^:]+):\s+(.*)$', line)
            if slot and keyValueSearch:
                output[slot][camelCase(keyValueSearch.group(1))] = keyValueSearch.group(2).strip()

    return {'output': output}

def register(main):
    main['lspci'] = {
        'cmd': 'lspci -mm -vvv',
        'description': 'List all PCI devices',
        'parser': parser
    }
