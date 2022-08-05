import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    slot = None
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            if line.strip() == "":
                continue

            slotSearch = re.search(r"^Slot:\s+(.*)$", line, re.IGNORECASE)
            if slotSearch:
                slot = slotSearch.group(1).strip()
                output[slot] = {}
                continue

            kv = re.search(r"^(\S[^:]+):\s+(.*)$", line)
            if slot and kv:
                key = camelCase(kv.group(1), to_camelcase)
                value = kv.group(2).strip()

                output[slot][key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["lspci"] = {
        "cmd": "lspci -mm -vvv",
        "description": "List all PCI devices",
        "parser": parser,
    }
