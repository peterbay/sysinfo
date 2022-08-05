import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {"processor": {}, "hardware": {}, "oth": {}}
    unprocessed = []

    if stdout:
        for block in re.split(r"\r\r|\n\n|\r\n\r\n", stdout):
            sub = {}
            for line in block.splitlines():
                kv = re.search(r"([^\t]+)\s*:\s*(.*)$", line)
                if kv:
                    key = camelCase(kv.group(1).strip(), to_camelcase)
                    value = kv.group(2).strip()

                    sub[key] = value
                    continue

                unprocessed.append(line)

            if "processor" in sub:
                output["processor"][sub["processor"]] = sub

            elif "hardware" in sub:
                output["hardware"] = sub

            else:
                output["oth"] = sub

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_cpuinfo",
            "system": ["linux"],
            "cmd": "cat /proc/cpuinfo",
            "description": "Type of processor used by your system",
            "parser": parser,
        }
    )
