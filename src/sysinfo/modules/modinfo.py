import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    moduleName = None
    unprocessed = []

    if stdout:
        stdout_fix = re.sub(r"\n[\t]+", " ", stdout)

        for line in stdout_fix.splitlines():
            kv = re.search(r"^([^:]+):\s+(.*)$", line)
            if kv:
                key = kv.group(1)
                value = kv.group(2)

                if key == ">>> moduleName":
                    moduleName = value
                    output[moduleName] = {}
                    continue

                if moduleName:
                    key = camelCase(key, to_camelcase)
                    output[moduleName][key] = value.strip()
                    continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "modinfo",
            "system": ["linux"],
            "cmd": """lsmod | grep -v "Module" | sed 's/ .*//g' | xargs -I {} -n 1 sh -c "echo '>>> moduleName: {}'; modinfo {}" """,
            "description": "Information about a Linux Kernel modules",
            "parser": parser,
        }
    )
