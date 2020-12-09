import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    moduleName = None
    if stdout:
        for line in stdout.splitlines():
            values = re.search(r'^([^:]+):\s+(.*)$', line)
            if not values:
                continue

            key = values.group(1)
            value = values.group(2)

            if key == 'moduleName':
                moduleName = value
                output[moduleName] = {}

            if moduleName:
                output[moduleName][key] = value.strip()


    return {'output': output}

def register(main):
    main['modinfo'] = {
        'cmd': """lsmod | grep -v "Module" | sed 's/ .*//g' | xargs -I {} -n 1 sh -c "echo 'moduleName: {}'; modinfo {}" """,
        'description': 'Information about a Linux Kernel modules',
        'parser': parser
    }
