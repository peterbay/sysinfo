import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
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

            if "name" in sub:
                output[sub["name"]] = sub

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_crypto"] = {
        "cmd": "cat /proc/crypto",
        "description": "Installed cryptographic ciphers used by the Linux kernel",
        "parser": parser,
    }
