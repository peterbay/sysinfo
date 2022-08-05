import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            values = re.search(r"^([^=]+)=(.*)$", line)
            if values:
                key = camelCase(values.group(1), to_camelcase)
                value = values.group(2).strip().strip('"')
                output[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["etc_release"] = {
        "cmd": "cat /etc/*release",
        "description": "OS release info",
        "parser": parser,
    }
