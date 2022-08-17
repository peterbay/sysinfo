import re
from sysinfo_lib import camelCase


def setPathValue(data, path, value):
    pathRest = None
    pathParts = re.search(r"^([^\/]+)\/?(.*)$", path)
    if pathParts:
        path = camelCase(pathParts.group(1))
        pathRest = pathParts.group(2)

    if not path in data:
        data[path] = {}

    if pathRest:
        setPathValue(data[path], pathRest, value)

    else:
        path = camelCase(path)
        if isinstance(data[path], dict):
            data[path] = []

        data[path].append(value)


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            pathValue = re.search(r"^\/proc\/fs\/([^:]+):(.*)$", line)
            if pathValue:
                path = pathValue.group(1)
                value = pathValue.group(2)

                print(path, value)
            #     if not re.search(r"^\s*#", value):
            #         setPathValue(output, path, value)

            #     continue

            # else:
            #     print(line)

            # unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_fs",
            "system": ["linux"],
            "cmd": """find /proc/fs -type f -follow -print | xargs grep "" """,
            "description": "File system parameters",
            "parser": parser,
        }
    )
