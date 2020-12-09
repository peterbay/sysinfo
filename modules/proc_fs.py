
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
        if isinstance(data[path], dict):
            data[path] = []
        data[path].append(value)

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            pathValue = re.search(r'^\/proc\/fs\/([^:]+):(.*)$', line)
            if pathValue:
                path = pathValue.group(1)
                value = pathValue.group(2)
                if not re.search(r'^\s*#', value):
                    setPathValue(output, path, value)

    return {'output': output}

def register(main):
    main['proc_fs'] = {
        'cmd': 'find /proc/fs -type f -follow -print | xargs grep ""',
        'description': 'File system parameters',
        'parser': parser
    }
