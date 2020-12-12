
import re

def parser(stdout, stderr):
    output = {}
    defaultUnit = None
    path = None
    if stdout:
        for line in stdout.splitlines():
            if line.strip() == '':
                defaultUnit = None
                path = None

            unitSearch = re.search(r'^(\S+);$', line)
            if unitSearch:
                defaultUnit = unitSearch.group(1)

            lineSplit = (line.strip(';') + (':' * 10)).split(':')

            if defaultUnit and re.search(r'^(\/[^:]+)', line):
                path = lineSplit[0]
                output[path] = {
                    'path': lineSplit[0],
                    'defaultUnit': defaultUnit,
                    'end': lineSplit[1],
                    'devType': lineSplit[2],
                    'sectorSize': lineSplit[3],
                    'physSectorSize': lineSplit[4],
                    'ptName': lineSplit[5],
                    'model': lineSplit[6],
                    'diskFlags': lineSplit[7],
                    'table': {}
                }

            if path and re.search(r'^(\d+):', line):
                output[path]['table'][lineSplit[0]] = {
                    'start': lineSplit[1],
                    'end': lineSplit[2],
                    'size': lineSplit[3],
                    'fileSystem': lineSplit[4],
                    'flags': lineSplit[5]
                }

    return {'output': output}

def register(main):
    main['parted'] = {
        'cmd': 'parted -m -l print',
        'description': 'Lists partition layout on all block devices',
        'parser': parser
    }
                                