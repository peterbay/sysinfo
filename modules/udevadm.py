import re
from sysinfo_lib import camelCase


def parse_looking_entry(line, entry, to_camelcase):
    key_value = re.search(r'^\s+([^=]+)=="([^"]*)"', line)
    if key_value:
        key = key_value.group(1).lower()
        value = key_value.group(2)

        multiple_values = re.match(r"^(\s+\d+)+$", value)
        if multiple_values:
            value = re.split(r"\s+", value.strip())

        key_attr = re.match(r"^(\S+){([^}]+)}", key, re.IGNORECASE)
        if key_attr:
            attrType = camelCase(key_attr.group(1), to_camelcase)

            if not attrType in entry:
                entry[attrType] = {}

            path = key_attr.group(2).split("/")

            if len(path) == 1:
                key_case = camelCase(path[0], to_camelcase)
                entry[attrType][key_case] = value

            else:
                sub_entry = entry[attrType]

                for part in path[0:-1]:
                    part_case = camelCase(part, to_camelcase)

                    if not part_case in sub_entry:
                        sub_entry[part_case] = {}

                    sub_entry = sub_entry[part_case]

                key_case = camelCase(path[-1], to_camelcase)
                sub_entry[key_case] = value

        else:
            entry[key] = value

        return True

    return False


def parser(stdout, stderr, to_camelcase):
    output = {"devices": {}, "parents": {}}
    types = {"P": "path", "N": "node", "L": "linkPriority", "E": "entry", "S": "link"}
    device = None
    parent = None
    looking_entry = None
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            deviceSearch = re.search(r"^>>> Device: (\S+)", line)
            if deviceSearch:
                device = deviceSearch.group(1)
                output["devices"][device] = {"parents": [], "entry": {}, "link": []}
                parent = None
                continue

            if not device:
                continue

            if line.strip() == "":
                looking_entry = None
                continue

            if re.match(
                r"^.*(Udevadm info starts|chain of parent|the udev rules|rule to match|single parent device)",
                line,
            ):
                continue

            keyValue = re.search(r"^(\S):\s+(.*)$", line)
            if keyValue:
                key = keyValue.group(1)
                value = keyValue.group(2).strip()
                if key in types:
                    key = types[key]

                if key == "entry":
                    valueSearch = re.search(r"^([^=]+)=(.*)$", value)
                    if valueSearch:
                        subkey = camelCase(valueSearch.group(1), to_camelcase)
                        subvalue = valueSearch.group(2).strip()
                        output["devices"][device]["entry"][subkey] = subvalue

                elif key == "link":
                    output["devices"][device]["link"].append(value)

                else:
                    output["devices"][device][key] = value

                continue

            deviceLook = re.search(r"^\s+looking at device \'([^\']+)", line)
            if deviceLook:
                looking_entry = output["devices"][device]
                continue

            parentDeviceLook = re.search(
                r"^\s+looking at parent device \'([^\']+)", line
            )
            if parentDeviceLook:
                parent = parentDeviceLook.group(1)
                output["devices"][device]["parents"].append(parent)

                if not parent in output["parents"]:
                    output["parents"][parent] = {}

                looking_entry = output["parents"][parent]
                continue

            if isinstance(looking_entry, dict):
                processed = parse_looking_entry(line, looking_entry, to_camelcase)
                if processed:
                    continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["udevadm"] = {
        "cmd": """udevadm info --export-db | grep "DEVNAME" | cut -d "=" -f2 | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; udevadm info --query=all --name={}; udevadm info --attribute-walk --name={}" """,
        "description": "Queries the udev database for device information stored in the udev database",
        "parser": parser,
    }

    main["udevadm_block_devices"] = {
        "cmd": """find /dev/ -type b | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; udevadm info --query=all --name={}; udevadm info --attribute-walk --name={}" """,
        "description": "Queries the udev database for block device information stored in the udev database",
        "parser": parser,
    }
