import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        device = ""
        for line in stdout.splitlines():
            dev = re.search(r"^>>> Device: (\S+)", line)
            if dev:
                device = dev.group(1)
                output[device] = {}
                continue

            kv = re.search(r"^(\w[^=]+)=(.*)$", line)
            if kv:
                key = camelCase(kv.group(1), to_camelcase)
                value = kv.group(2)
                output[device][key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "blkid",
            "system": ["linux"],
            "cmd": """blkid -o device | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; blkid -o export -p {}; blkid -o export -i {}" """,
            "description": "Block device attributes",
            "parser": parser,
        }
    )
