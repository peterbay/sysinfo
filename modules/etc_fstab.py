
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            if re.match(r'^\s*#', line):
                continue
            lineMatch = re.split(r'\s+', line)
            if lineMatch and len(lineMatch) > 5:
                output[lineMatch[0]] = {
                    'location': lineMatch[0],
                    'mountPoint': lineMatch[1],
                    'type': lineMatch[2],
                    'security': lineMatch[3],
                    'dump': lineMatch[4],
                    'fsckOrder': lineMatch[5]
                }
    
    return {'output': output}

def register(main):
    main['etc_fstab'] = {
        'cmd': 'cat /etc/fstab',
        'description': 'Filesystems mounted on boot',
        'parser': parser
    }