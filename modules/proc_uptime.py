import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        splitted = re.split(r'\s+', stdout.strip())
        if len(splitted) > 0:
            output['systemUp'] = splitted[0]

        if len(splitted) > 1:
            output['sumCoresIdle'] = splitted[1]

    return {'output': output}

def register(main):
    main['proc_uptime'] = {
        'cmd': 'cat /proc/uptime',
        'description': 'Information detailing how long the system has been on since its last restart',
        'parser': parser
    }