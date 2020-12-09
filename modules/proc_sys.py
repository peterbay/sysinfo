
import re

def setPathValue(data, path, value):
    pathRest = None
    pathParts = re.search(r'^([^\/]+)\/?(.*)$', path)
    if pathParts:
        path = pathParts.group(1)
        pathRest = pathParts.group(2)

    if not path in data:
        data[path] = {}

    if pathRest:
        setPathValue(data[path], pathRest, value)
    else:
        data[path] = value

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            pathValue = re.search(r'^\/proc\/sys\/([^:]+):(.*)$', line)
            if pathValue:
                path = pathValue.group(1)
                value = pathValue.group(2)
                if value.strip() == '':
                    continue
                if not re.search(r'^\s*#', value):
                    setPathValue(output, path, value)

    return {'output': output}

def register(main):
    main['proc_sys'] = {
        'cmd': """find /proc/sys -type f -follow -print 2>/dev/null | xargs -n 1 -I {} sh -c 'VAL=$(cat {} 2>/dev/null); echo {}:$VAL;'""",
        'description': 'Information about the system and kernel features',
        'parser': parser
    }