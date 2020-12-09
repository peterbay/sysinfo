
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            keyValueSearch = re.search(r'^\s*([^:]+):\s*(.*)$', line)
            if keyValueSearch:
                output[keyValueSearch.group(1)] = keyValueSearch.group(2).strip()

    return {'output': output}

def register(main):
    main['proc_dma'] = {
        'cmd': 'cat /proc/dma',
        'description': 'List of the registered ISA DMA channels in use',
        'parser': parser
    }