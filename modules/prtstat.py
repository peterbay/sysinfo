
import re

def parser(stdout, stderr):
    output = {}
    pid = ''
    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.findall(r'(\S+):\s(\S+)', line)
            for kv in lineMatch:
                if kv[0] == 'pid':
                    pid = kv[1]
                    output[pid] = {}

                if pid != '':
                    output[pid][kv[0]] = kv[1]

    return {'output': output}

def register(main):
    main['prtstat'] = {
        'cmd': 'ps -eo pid | xargs -I {} prtstat -r {}',
        'description': 'Print statistics of a processes',
        'parser': parser
    }