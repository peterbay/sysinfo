import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            kv = re.search(r"^(\S+)\s*(.*)$", line)
            if kv:
                key = camelCase(kv.group(1), to_camelcase)
                value = kv.group(2).strip()

                output[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["getconf"] = {
        "cmd": "getconf -a",
        "description": "Configuration variables for the current system and their values",
        "parser": parser,
    }
