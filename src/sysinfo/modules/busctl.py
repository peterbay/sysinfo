import re
from sysinfo_lib import parseTable, camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    if stdout:
        output = parseTable(stdout, to_camelcase=to_camelcase)

    return {"output": output, "unprocessed": []}


def parser_tree(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        name = ""
        for line in stdout.splitlines():
            header = re.search(r"^(\S+) (.+):", line)

            if header:
                name = header.group(2)
                output[name] = []
                continue

            tree = re.search(r"^\/(.+)$", line)
            if tree and name:
                output[name].append(tree.group(1))
                continue

            if line == "" or line == "/":
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def parser_status(stdout, stderr, to_camelcase):
    output = {}
    key = ""
    is_array = False
    unprocessed = []

    if stdout:
        device = ""
        for line in stdout.splitlines():
            dev = re.search(r"^>>> Device: (\S+)", line)
            if dev:
                device = dev.group(1)
                output[device] = {}
                key = ""
                is_array = False
                continue

            kv = re.search(r"^(\w[^=]+)=(.*)$", line)
            if kv:
                key = camelCase(kv.group(1), to_camelcase)
                value = kv.group(2).strip()

                if re.match(r"^cap_", value):
                    is_array = True
                    output[device][key] = value.split(r" ")
                    print(value.split(r" "))

                else:
                    output[device][key] = value

                continue

            cont = re.search(r"^\s\s+(.*)$", line)
            if cont and key and is_array:
                key = camelCase(key, to_camelcase)
                output[device][key] += cont.group(1).strip().split(r" ")
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "busctl",
            "system": ["linux"],
            "cmd": "busctl --no-pager | column -t",
            "description": "Introspect the bus",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "busctl_tree",
            "system": ["linux"],
            "cmd": "busctl --no-pager --list tree",
            "description": "Object tree for services",
            "parser": parser_tree,
        }
    )

    main.register(
        {
            "name": "busctl_status",
            "system": ["linux"],
            "cmd": """busctl list | awk '!/^(NAME)/ {print $1}' | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; busctl --no-pager status {}" """,
            "description": "Process information and credentials of a bus service",
            "parser": parser_status,
        }
    )
