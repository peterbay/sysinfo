
import re

def parser(stdout, stderr):
    output = []
    if stdout:
        for line in stdout.splitlines():
            values = re.search(r'^\s*([^#]+)', line)
            if not values:
                continue
            value = values.group(1).strip()
            if value != '':
                output.append(value)

    return {'output': output}

def register(main):
    main['etc_locale_gen'] = {
        'cmd': 'cat /etc/locale.gen',
        'description': 'Configuration file for locale-gen',
        'parser': parser
    }
