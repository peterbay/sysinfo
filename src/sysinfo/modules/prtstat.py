import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    pid = ""
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            processed = False
            pairs = re.findall(r"(\S+):\s(\S+)", line)
            for kv in pairs:
                if kv[0] == "pid":
                    pid = kv[1]
                    output[pid] = {}

                if pid != "":
                    key = camelCase(kv[0], to_camelcase)
                    value = kv[1].strip()

                    output[pid][key] = value
                    processed = True

            if not processed:
                unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "prtstat",
            "system": ["linux"],
            "cmd": "ps -eo pid | xargs -I {} prtstat -r {}",
            "description": "Print statistics of a processes",
            "parser": parser,
        }
    )
