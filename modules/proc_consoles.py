
import re

def parser(stdout, stderr):
    """
        The columns are:
        device              name of the device
        operations          R = can do read operations
                            W = can do write operations
                            U = can do unblank
        flags               E = it is enabled
                            C = it is preferred console
                            B = it is primary boot console
                            p = it is used for printk buffer
                            b = it is not a TTY but a Braille device
                            a = it is safe to use when cpu is offline
        major:minor         major and minor number of the device separated by a colon
    """

    output = {}
    if stdout:
        for line in stdout.splitlines():
            values = re.search(r'^(\S+)\s+(.*)\s+(\S+):(\S+)', line)
            if values:
                params = values.group(2).strip()
                output[values.group(1)] = {
                    'device': values.group(1),
                    'operations': {
                        'read': 'R' in params,
                        'write': 'W' in params,
                        'unblank': 'U' in params,
                    },
                    'flags': {
                        'enabled': 'E' in params,
                        'preferred': 'C' in params,
                        'primaryBoot': 'B' in params,
                        'printkBuffer': 'p' in params,
                        'braile': 'b' in params,
                        'safeCpuOffline': 'a' in params,
                    },
                    'major': values.group(3),
                    'minor': values.group(4)
                }

    return {'output': output}

def register(main):
    main['proc_consoles'] = {
        'cmd': 'cat /proc/consoles',
        'description': 'Information about current consoles including tty',
        'parser': parser
    }
