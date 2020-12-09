import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r'^([^\s+]+)\s(.*)$', line)
            if lineMatch:
                output[lineMatch.group(1)] = lineMatch.group(2)

    return {'output': output}

def register(main):
    main['proc_vmstat'] = {
        'cmd': 'cat /proc/vmstat',
        'description': 'Detailed virtual memory statistics from the kernel',
        'parser': parser
    }
