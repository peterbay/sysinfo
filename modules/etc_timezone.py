
def parser(stdout, stderr):
    output = ''
    if stdout:
        output = stdout.strip()
    return {'output': output}

def register(main):
    main['etc_timezone'] = {
        'cmd': 'cat /etc/timezone',
        'description': 'Timezone settings',
        'parser': parser
    }
