
import re

def parser(stdout, stderr):
    output = []
    if stdout:
        for line in stdout.splitlines():
            values = re.search(r'^\s*([^-]+)-(\S+)\s*:\s*(.*)$', line)
            if values:
                output.append({
                    'from': values.group(1),
                    'to': values.group(2),
                    'device': values.group(3)
                })

    return {'output': output}

def register(main):
    main['proc_iomem'] = {
        'cmd': 'cat /proc/iomem',
        'description': """Map of the system's memory for each physical device""",
        'parser': parser
    }