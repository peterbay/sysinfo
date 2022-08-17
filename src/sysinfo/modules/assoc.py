import re
from sysinfo_lib import parseTable, tableToDict, camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        device = ""
        for line in stdout.splitlines():
            kv = re.search(r"^([^=]+)=(.*)$", line)
            if kv:
                key = kv.group(1)
                value = kv.group(2)
                output[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "assoc",
            "system": ["windows"],
            "cmd": "assoc",
            "description": "File associations",
            "parser": parser,
        }
    )
