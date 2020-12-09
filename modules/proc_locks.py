
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            lineSplit = re.split(r'[\s\t]+', line)
            if lineSplit and len(lineSplit) > 5:
                output[lineSplit[0]] = {
                    'uid': lineSplit[0],
                    'class': lineSplit[1],
                    'lockType': lineSplit[2],
                    'allowAccessType': lineSplit[3],
                    'pid': lineSplit[4],
                    'fileID': lineSplit[5],
                    'lockedRegion': lineSplit[6]
                }

    return {'output': output}

def register(main):
    main['proc_locks'] = {
        'cmd': 'cat /proc/locks',
        'description': 'Files currently locked by the kernel',
        'parser': parser
    }