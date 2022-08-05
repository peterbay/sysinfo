import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            kv = re.search(r"^([^:]+):\s*(.*)$", line, re.IGNORECASE)
            if kv:
                key = camelCase(kv.group(1).strip(":"), to_camelcase)
                value = kv.group(2).strip()

                valueSearch = re.search(r"(.*)\s+(.*)$", value)
                if valueSearch:
                    output[key] = {
                        "value": valueSearch.group(1),
                        "type": valueSearch.group(2),
                    }
                else:
                    output[key] = {"value": value, "type": ""}

                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": []}


def register(main):
    main["proc_meminfo"] = {
        "cmd": "cat /proc/meminfo",
        "description": "Reports a large amount of valuable information about the systems RAM usage",
        "parser": parser,
    }
