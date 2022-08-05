import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r"^([^\s+]+)\s(.*)$", line)
            if lineMatch:
                key = camelCase(lineMatch.group(1), to_camelcase)
                value = lineMatch.group(2)

                output[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_vmstat",
            "system": ["linux"],
            "cmd": "cat /proc/vmstat",
            "description": "Detailed virtual memory statistics from the kernel",
            "parser": parser,
        }
    )
