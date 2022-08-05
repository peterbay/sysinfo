import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {"nodes": {}}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            row = re.search(r"Node\s([^,]+),\szone\s+(\S+)\s*(.*)$", line)
            if row:
                node = row.group(1)
                zone = row.group(2)
                value = re.split(r"\s+", row.group(3).strip())

                if not node in output["nodes"]:
                    output["nodes"][node] = {}

                output["nodes"][node][zone] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_buddyinfo"] = {
        "cmd": "cat /proc/buddyinfo",
        "description": "Memory fragmentation",
        "parser": parser,
    }
