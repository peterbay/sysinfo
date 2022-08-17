import re
from sysinfo_lib import camelCase


def set_path_value(data, path, value, to_camelcase):
    pathRest = None
    pathParts = re.search(r"^([^\.]+)\.?(.*)$", path)
    if pathParts:
        path = camelCase(pathParts.group(1), to_camelcase)
        pathRest = pathParts.group(2)

    if not path in data:
        data[path] = {}

    if pathRest:
        set_path_value(data[path], pathRest, value, to_camelcase)
    else:
        data[path] = value


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            kv = re.search(r"^([^=]+)=(.*)$", line)
            if kv:
                key = kv.group(1).strip()
                value = kv.group(2).strip()

                set_path_value(output, key, value, to_camelcase)
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "sysctl",
            "system": ["linux"],
            "cmd": "sysctl -a -e",
            "description": "Runtime kernel parameters",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "sysctl_system",
            "system": ["linux"],
            "cmd": "sysctl -a -e --system",
            "description": "Runtime kernel parameters from all system configuration files",
            "parser": parser,
        }
    )
