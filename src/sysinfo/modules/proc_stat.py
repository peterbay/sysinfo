import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        for line in stdout.splitlines():
            parts = re.split(r"\s+", line)
            key = parts.pop(0)

            if re.match(r"^cpu", key) and len(parts) == 10:
                output[key] = {
                    "user": parts[0],
                    "nice": parts[1],
                    "system": parts[2],
                    "idle": parts[3],
                    "iowait": parts[4],
                    "irq": parts[5],
                    "softirq": parts[6],
                    "steal": parts[7],
                    "guest": parts[8],
                    "guest_nice": parts[9],
                }
                continue

            output[key] = " ".join(parts)

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "proc_stat",
            "system": ["linux"],
            "cmd": "cat /proc/stat",
            "description": "Kernel/system statistics",
            "parser": parser,
        }
    )
