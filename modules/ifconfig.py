
import re
from sysinfo_lib import camelCase

def extractValue(data, line, key, regExp):
    search = re.search(regExp, line, re.IGNORECASE)
    if search:
        data[key] = search.group(1)
    return data

def extractValues(data, line):
    for pair in re.split(r'\s\s+', line):
        desc = re.search(r'^\((.*)\)$', pair.strip())
        if desc:
            data['description'] = desc.group(1)
            continue

        kv = re.search(r'^([^\s]+)\s(\S.*)$', pair)
        if kv:
            data[kv.group(1)] = kv.group(2)

    return extractValues

def parser(stdout, stderr):
    output = {}
    blockData = {}
    if stdout:
        for block in re.split(r'\r\r|\n\n|\r\n\r\n', stdout):
            blockData = {'entries': [], 'rx': {}, 'tx': {}}
            for line in block.splitlines():
                header = re.search(r'^(\S[^:]+):\s*(.*)$', line)
                if header:
                    name = header.group(1)
                    blockData['name'] = name
                    extractValue(blockData, line, 'flags', r'flags=(\S+)')
                    extractValues(blockData, header.group(2))
                    output[name] = blockData

                rxTx = re.search(r'^\s+([rt]x)\s+(.*)$', line, re.IGNORECASE)
                if rxTx:
                    type = rxTx.group(1).lower()
                    extractValues(blockData[type], rxTx.group(2))
                    continue

                sub = re.search(r'^\s+(\S+)\s\s(.*)$', line, re.IGNORECASE)
                if sub:
                    subData = {'type': sub.group(1)}
                    extractValues(subData, sub.group(2))
                    blockData['entries'].append(subData)
                    continue

                sub = re.search(r'^\s+(\S+)\s(\S+)\s\s(.*)$', line, re.IGNORECASE)
                if sub:
                    subData = {'type': sub.group(1), 'value': sub.group(2)}
                    extractValues(subData, sub.group(3))
                    blockData['entries'].append(subData)

    return {'output': output}

def register(main):
    main['ifconfig'] = {
        'cmd': 'ifconfig -a -v',
        'description': 'List all interfaces which are currently available, even if down',
        'parser': parser
    }
