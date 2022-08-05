import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r"^([^:]+):\s*(.*)", line)
            if lineMatch:
                key = camelCase(lineMatch.group(1).strip(), to_camelcase)
                value = lineMatch.group(2).strip()

                output[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["timedatectl"] = {
        "cmd": "timedatectl status",
        "description": "System time and date",
        "parser": parser,
    }

    main["timedatectl_timesync"] = {
        "cmd": "timedatectl timesync-status",
        "description": "Status of systemd-timesyncd.service",
        "parser": parser,
    }
