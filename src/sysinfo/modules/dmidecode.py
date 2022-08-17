import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    dmiSections = {
        "0": "BIOS",
        "1": "System",
        "2": "Base Board",
        "3": "Chassis",
        "4": "Processor",
        "5": "Memory Controller",
        "6": "Memory Module",
        "7": "Cache",
        "8": "Port Connector",
        "9": "System Slots",
        "10": "On Board Devices",
        "11": "OEM Strings",
        "12": "System Configuration Options",
        "13": "BIOS Language",
        "14": "Group Associations",
        "15": "System Event Log",
        "16": "Physical Memory Array",
        "17": "Memory Device",
        "18": "32-bit Memory Error",
        "19": "Memory Array Mapped Address",
        "20": "Memory Device Mapped Address",
        "21": "Built-in Pointing Device",
        "22": "Portable Battery",
        "23": "System Reset",
        "24": "Hardware Security",
        "25": "System Power Controls",
        "26": "Voltage Probe",
        "27": "Cooling Device",
        "28": "Temperature Probe",
        "29": "Electrical Current Probe",
        "30": "Out-of-band Remote Access",
        "31": "Boot Integrity Services",
        "32": "System Boot",
        "33": "64-bit Memory Error",
        "34": "Management Device",
        "35": "Management Device Component",
        "36": "Management Device Threshold Data",
        "37": "Memory Channel",
        "38": "IPMI Device",
        "39": "Power Supply",
        "40": "Additional Information",
        "41": "Onboard Devices Extended Information",
        "42": "Management Controller Host Interface",
        "126": "Disabled entry",
        "127": "End of table",
    }
    handle = None
    output = {}
    unprocessed = []

    if stdout:

        # fix multiline
        stdout = re.sub(r"\n\t\t", " ", stdout)

        for line in stdout.splitlines():
            if line.strip() == "":
                handle = None

            handleSearch = re.search(
                r"^Handle\s+([^,]+),\s+DMI type\s+([^,]+),", line, re.IGNORECASE
            )
            if handleSearch:
                handle = handleSearch.group(1)
                dmiType = handleSearch.group(2)
                intDmiType = int(dmiType)

                if intDmiType > 127 and intDmiType < 256:
                    output[handle] = {"__dmiType": dmiType, "__section": "OEM Specific"}
                    continue

                if dmiType in dmiSections:
                    output[handle] = {
                        "__dmiType": dmiType,
                        "__section": dmiSections[dmiType],
                    }
                    continue

                output[handle] = {"__dmiType": dmiType, "__section": "Unknown"}
                continue

            if handle and re.match(r"^\S", line):
                output[handle]["__type"] = line
                continue

            entry = re.search(r"^\s+([^:]+):\s+(.*)$", line)
            if handle and entry:
                key = camelCase(entry.group(1), to_camelcase)
                value = entry.group(2).strip()

                output[handle][key] = value
                continue

            if line == "":
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "dmidecode",
            "system": ["linux"],
            "cmd": "dmidecode",
            "description": "Dumping all information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_bios",
            "system": ["linux"],
            "cmd": "dmidecode -t bios",
            "description": "Dumping BIOS information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_system",
            "system": ["linux"],
            "cmd": "dmidecode -t system",
            "description": "Dumping SYSTEM information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_baseboard",
            "system": ["linux"],
            "cmd": "dmidecode -t baseboard",
            "description": "Dumping BASEBOARD information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_chassis",
            "system": ["linux"],
            "cmd": "dmidecode -t chassis",
            "description": "Dumping CHASSIS information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_processor",
            "system": ["linux"],
            "cmd": "dmidecode -t processor",
            "description": "Dumping CHASSIS information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_memory",
            "system": ["linux"],
            "cmd": "dmidecode -t memory",
            "description": "Dumping MEMORY information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_cache",
            "system": ["linux"],
            "cmd": "dmidecode -t cache",
            "description": "Dumping CACHE information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_connector",
            "system": ["linux"],
            "cmd": "dmidecode -t connector",
            "description": "Dumping CONNECTOR information from DMI (SMBIOS)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "dmidecode_slot",
            "system": ["linux"],
            "cmd": "dmidecode -t slot",
            "description": "Dumping SLOT information from DMI (SMBIOS)",
            "parser": parser,
        }
    )
