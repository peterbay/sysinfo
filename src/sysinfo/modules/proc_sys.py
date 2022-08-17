import re
from sysinfo_lib import camelCase


def setPathValue(data, path, value, to_camelcase):
    pathRest = None
    pathParts = re.search(r"^([^\/]+)\/?(.*)$", path)
    if pathParts:
        path = camelCase(pathParts.group(1), to_camelcase)
        pathRest = pathParts.group(2)

    else:
        path = camelCase(path)

    if not path in data:
        data[path] = {}

    if pathRest:
        setPathValue(data[path], pathRest, value, to_camelcase)
    else:
        key = camelCase(path, to_camelcase)
        data[key] = value


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            pathValue = re.search(r"^\/proc\/sys\/([^:]+):(.*)$", line)
            if pathValue:
                path = pathValue.group(1)
                value = pathValue.group(2)
                setPathValue(output, path, value, to_camelcase)
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_sys",
            "system": ["linux"],
            "cmd": """find /proc/sys -type f -follow -print 2>/dev/null | xargs -n 1 -I {} sh -c 'VAL=$(cat {} 2>/dev/null); echo {}:$VAL;'""",
            "description": "Information about the system and kernel features",
            "parser": parser,
        }
    )
