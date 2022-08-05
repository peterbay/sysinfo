import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        for kv in re.split(r"[\s\t]+", stdout.strip()):
            splitted = re.search(r"^([^=]+)=(.*)$", kv)
            if splitted:
                key = camelCase(splitted.group(1), to_camelcase)
                value = splitted.group(2)

            else:
                key = kv
                value = ""

            if key in output:
                if isinstance(output[key], str):
                    output[key] = [output[key]]

                output[key].append(value)

            else:
                output[key] = value

    return {"output": output, "unprocessed": []}


def register(main):
    main["proc_cmdline"] = {
        "cmd": "cat /proc/cmdline",
        "description": "Parameters passed to the kernel at the time it is started",
        "parser": parser,
    }
