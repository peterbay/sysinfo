import re
from sysinfo_lib import parseTable, tableToDict, camelCase


def parser(stdout, stderr, to_camelcase):
    output = parseTable(
        stdout,
        header_pattern=r"^(Address\s+)\s(HWtype\s+)\s(HWaddress\s+)\s(Flags Mask\s+)\s(Iface\s*)",
        to_camelcase=to_camelcase,
    )

    return {"output": output, "unprocessed": []}


def parser_win(stdout, stderr, to_camelcase):
    output = []
    unprocessed = []
    interface = None

    if stdout:
        for line in stdout.splitlines():
            interface_match = re.search(r"^Interface:\s*(\S+)\s*---\s*(\S+)$", line)
            if interface_match:
                interface = {
                    "ip": interface_match.group(1).strip(),
                    "id": interface_match.group(2).strip(),
                    "entries": [],
                }
                output.append(interface)
                continue

            if re.match(r"^.*Physical\s*Address", line, re.IGNORECASE):
                continue

            entry_match = re.search(r"^\s+(\S+)\s+(\S+)\s+(\S+)", line)
            if entry_match and interface:
                interface["entries"].append(
                    {
                        "intenetAddress": entry_match.group(1).strip(),
                        "physicalAddress": entry_match.group(2).strip(),
                        "type": entry_match.group(3).strip(),
                    }
                )
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "arp",
            "system": ["linux"],
            "cmd": "arp",
            "description": "System ARP cache",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "arp",
            "system": ["windows"],
            "cmd": "%SystemRoot%\\system32\\arp -a",
            "description": "System ARP cache",
            "parser": parser_win,
        }
    )
