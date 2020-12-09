
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            kv = re.search(r'^(\S+)\s*(.*)$', line)
            if kv:
                output[kv.group(1)] = kv.group(2).strip()

    return {
        'output': output,
        }

def register(main):
    main['getconf'] = {
        'cmd': 'getconf -a',
        'description': 'Configuration variables for the current system and their values',
        'parser': parser
    }