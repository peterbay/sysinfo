import re
from sysinfo_lib import camelCase


def extract_params(entry, params, to_camelcase):
    patterns = [
        r"(\S[^=]+)=(\S+)",
        r'(\S[^=]+)=\"([^"]*)\"',
        r"(\S[^=]+)=(\s|$)",
    ]

    for pattern in patterns:
        kv = re.findall(pattern, params)
        if kv:
            for pair in kv:
                key = camelCase(pair[0], to_camelcase)
                value = pair[1]
                entry[key] = value


def parser(stdout, stderr, to_camelcase):
    output = {"devices": [], "handlers": {}}
    unprocessed = []
    types = {
        "I": "deviceId",
        "N": "name",
        "P": "physicalPath",
        "S": "sysfsPath",
        "U": "uid",
        "H": "inputHandlers",
        "B": "bitmaps",
    }

    if stdout:
        [devices, handlers] = stdout.split(">>> handlers")

        print(devices)

        for block in re.split(r"\r\r|\n\n|\r\n\r\n", devices):
            blockData = {}

            for line in block.splitlines():
                parts = re.search(r"^(\w):\s+(.*)$", line)
                if parts:
                    type = parts.group(1).strip()
                    params = parts.group(2).strip()

                    if type in types:
                        type_label = types[type]
                        if not type_label in blockData:
                            blockData[type_label] = {}

                        extract_params(blockData[type_label], params, to_camelcase)

            output["devices"].append(blockData)

        for line in handlers.splitlines():
            line = re.sub(r"^N: ", "", line)

            kv = re.findall(r"(\S[^=]+)=(\S+)", line)
            if kv:
                entry = {}
                for pair in kv:
                    key = camelCase(pair[0], to_camelcase)
                    value = pair[1]
                    entry[key] = value

                if "name" in entry:
                    output["handlers"][entry["name"]] = entry

                if "Name" in entry:
                    output["handlers"][entry["Name"]] = entry

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_bus_input"] = {
        "cmd": 'cat /proc/bus/input/devices; echo ">>> handlers"; cat /proc/bus/input/handlers;',
        "description": "Input devices",
        "parser": parser,
    }
