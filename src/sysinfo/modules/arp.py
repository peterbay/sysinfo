import re
from sysinfo_lib import parseTable, tableToDict, camelCase


def parser(stdout, stderr, to_camelcase):
    output = parseTable(
        stdout,
        header_pattern=r"^(Address\s+)\s(HWtype\s+)\s(HWaddress\s+)\s(Flags Mask\s+)\s(Iface\s*)",
        to_camelcase=to_camelcase,
    )

    return {"output": output, "unprocessed": []}


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
