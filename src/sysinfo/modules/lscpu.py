import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            line = re.sub(r"\(s\)", "s", line)
            kv = re.search(r"^([^:]+):\s*(.*)", line)
            if kv:
                key = camelCase(kv.group(1), to_camelcase)
                value = kv.group(2)

                output[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["lscpu"] = {
        "cmd": "lscpu",
        "description": "Information about the CPU architecture",
        "parser": parser,
    }