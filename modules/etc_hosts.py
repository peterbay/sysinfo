
import re

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            values = re.search(r'^\/etc\/([^\:]+):\s*(.*)$', line)
            if not values:
                continue
            group = values.group(1)
            value = re.sub(r'#.*$', '', values.group(2)).strip()
            if group not in output:
                output[group] = []
            if value != '':
                output[group].append(value.split('\t'))

    return {'output': output}

def register(main):
    main['etc_hosts'] = {
        'cmd': """grep "" /etc/hosts*""",
        'description': 'Maps hostnames to IP addresses',
        'parser': parser
    }
