
import re
from sysinfo_lib import camelCase


def parser(stdout, stderr):
    output = {}
    ignoredLines = []
    if stdout:
        device = ''
        for line in stdout.splitlines():
            dev = re.search(r'^>>> Device: (\S+)', line)
            kv = re.search(r'^(\w[^=]+)=(.*)$', line)
            if dev:
                device = dev.group(1)
                output[device] = {}
            elif kv:
                output[device][camelCase(kv.group(1))] = kv.group(2)
            else:
                ignoredLines.append(line)
                pass

    return {
        'output': output,
        'ignored': ignoredLines
        }

def register(main):
    main['blkid'] = {
        'cmd': """blkid -o device | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; blkid -o export -p {}; blkid -o export -i {}" """,
        'description': 'Block device attributes',
        'parser': parser
    }