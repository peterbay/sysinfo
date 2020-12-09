
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    deviceType = None
    if stdout:
        for line in stdout.splitlines():
            dt = re.search(r'^([^:]+):', line)
            if dt:
                deviceType = camelCase(dt.group(1))
                output[deviceType] = {}

            dv = re.search(r'^\s*(\d+)\s*(.*)$', line)
            if dv and deviceType:
                id = dv.group(1)
                name = dv.group(2)
                if not name in output[deviceType]:
                    output[deviceType][name] = []

                output[deviceType][name].append(id)

    return {'output': output}

def register(main):
    main['proc_devices'] = {
        'cmd': 'cat /proc/devices',
        'description': 'Installed cryptographic ciphers used by the Linux kernel',
        'parser': parser
    }
