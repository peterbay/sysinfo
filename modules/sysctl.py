
import re

def setPathValue(data, path, value):
    pathRest = None
    pathParts = re.search(r'^([^\.]+)\.?(.*)$', path)
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
            kv = re.search(r'^([^=]+)=(.*)$', line)
            if kv:
                key = kv.group(1).strip()
                value = kv.group(2).strip()
                setPathValue(output, key, value)

    return {'output': output}

def register(main):
    main['sysctl'] = {
        'cmd': 'sysctl -a -e',
        'description': 'Runtime kernel parameters',
        'parser': parser
    }
    main['sysctl_system'] = {
        'cmd': 'sysctl -a -e --system',
        'description': 'Runtime kernel parameters from all system configuration files',
        'parser': parser
    }
