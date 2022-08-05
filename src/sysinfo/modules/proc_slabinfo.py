import re
from sysinfo_lib import camelCase


def extract_key_value(keys, data):
    entry = {}

    if len(keys) == len(data):
        for key_index, key in enumerate(keys):
            entry[key] = data[key_index]

    return entry


def parser(stdout, stderr, to_camelcase):
    output = {}
    key_names = []
    has_keys = False
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            if re.match(r"^slabinfo - version", line):
                continue

            header = re.search(r"^# name\s+(.*)$", line)
            if header:
                parts = header.group(1).strip().split(":")
                for part in parts:
                    part = part.strip()
                    part = re.sub(r"(tunables|slabdata)\s+", "", part)
                    part = part.replace("<", "").replace(">", "")
                    part_columns = re.split(r"\s+", part)
                    part_columns = [
                        camelCase(key, to_camelcase) for key in part_columns
                    ]

                    key_names.append(part_columns)

                has_keys = True
                continue

            row = re.search(r"^(\S+)\s+(.*)\s:\stunables(.*)\s:\sslabdata(.*)$", line)
            if has_keys and row:
                name = row.group(1)
                statistics_data = re.split(r"\s+", row.group(2).strip())
                tunables_data = re.split(r"\s+", row.group(3).strip())
                slabdata_data = re.split(r"\s+", row.group(4).strip())

                statistics = extract_key_value(key_names[0], statistics_data)
                tunables = extract_key_value(key_names[1], tunables_data)
                slabdata = extract_key_value(key_names[2], slabdata_data)

                output[name] = {
                    "statistics": statistics,
                    "tunables": tunables,
                    "slabdata": slabdata,
                }
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_slabinfo",
            "system": ["linux"],
            "cmd": "cat /proc/slabinfo",
            "description": "Kernel caches informations",
            "parser": parser,
        }
    )
