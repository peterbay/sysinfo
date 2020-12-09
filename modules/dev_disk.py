
import re

def parser(stdout, stderr):
    output = {'all': {}}
    if stdout:
        typeName = ''
        for line in stdout.splitlines():
            matchType = re.search(r'^\/dev\/disk\/by-(.*):\s*$', line)
            if matchType:
                typeName = matchType.group(1)
                output[typeName] = {}

            matchEntry = re.search(r'\s(\S+)\s+->\s+[\.\/]+(.*)$', line)
            if matchEntry and typeName:
                key = matchEntry.group(1).strip()
                value = matchEntry.group(2).strip()
                output[typeName][key] = value
                
                if not value in output['all']:
                    output['all'][value] = {}
                
                output['all'][value][typeName] = key

    return {'output': output}

def register(main):
    main['dev_disk'] = {
        'cmd': 'ls -l /dev/disk/by-*',
        'description': 'Disk devices mapping',
        'parser': parser
    }
