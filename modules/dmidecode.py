
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    dmiSections = {
        '0': 'BIOS',
        '1': 'System',
        '2': 'Base Board',
        '3': 'Chassis',
        '4': 'Processor',
        '5': 'Memory Controller',
        '6': 'Memory Module',
        '7': 'Cache',
        '8': 'Port Connector',
        '9': 'System Slots',
        '10': 'On Board Devices',
        '11': 'OEM Strings',
        '12': 'System Configuration Options',
        '13': 'BIOS Language',
        '14': 'Group Associations',
        '15': 'System Event Log',
        '16': 'Physical Memory Array',
        '17': 'Memory Device',
        '18': '32-bit Memory Error',
        '19': 'Memory Array Mapped Address',
        '20': 'Memory Device Mapped Address',
        '21': 'Built-in Pointing Device',
        '22': 'Portable Battery',
        '23': 'System Reset',
        '24': 'Hardware Security',
        '25': 'System Power Controls',
        '26': 'Voltage Probe',
        '27': 'Cooling Device',
        '28': 'Temperature Probe',
        '29': 'Electrical Current Probe',
        '30': 'Out-of-band Remote Access',
        '31': 'Boot Integrity Services',
        '32': 'System Boot',
        '33': '64-bit Memory Error',
        '34': 'Management Device',
        '35': 'Management Device Component',
        '36': 'Management Device Threshold Data',
        '37': 'Memory Channel',
        '38': 'IPMI Device',
        '39': 'Power Supply'
    }
    section = None
    output = {}

    if stdout:
        for line in stdout.splitlines():
            if line.strip() == '':
                section = None
            
            handleSearch = re.search(r'^Handle\s+([^,]+),\s+DMI type\s+([^,]+),', line, re.IGNORECASE)
            if handleSearch:
                handle = handleSearch.group(1)
                dmiType = handleSearch.group(2)
                if dmiType in dmiSections:
                    section = camelCase(dmiSections[dmiType])
                    output[section] = {
                        '__handle': handle,
                        '__dmiType': dmiType
                    }

            entry = re.search(r'^\s+([^:]+):\s+(.*)$', line)
            if section and entry:
                output[section][camelCase(entry.group(1))] = entry.group(2).strip()

    return {'output': output}

def register(main):
    main['dmidecode'] = {
        'cmd': 'dmidecode',
        'description': 'Dumping all information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_bios'] = {
        'cmd': 'dmidecode -t bios',
        'description': 'Dumping BIOS information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_system'] = {
        'cmd': 'dmidecode -t system',
        'description': 'Dumping SYSTEM information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_baseboard'] = {
        'cmd': 'dmidecode -t baseboard',
        'description': 'Dumping BASEBOARD information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_chassis'] = {
        'cmd': 'dmidecode -t chassis',
        'description': 'Dumping CHASSIS information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_processor'] = {
        'cmd': 'dmidecode -t processor',
        'description': 'Dumping CHASSIS information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_memory'] = {
        'cmd': 'dmidecode -t memory',
        'description': 'Dumping MEMORY information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_cache'] = {
        'cmd': 'dmidecode -t cache',
        'description': 'Dumping CACHE information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_connector'] = {
        'cmd': 'dmidecode -t connector',
        'description': 'Dumping CONNECTOR information from DMI (SMBIOS)',
        'parser': parser
    }

    main['dmidecode_slot'] = {
        'cmd': 'dmidecode -t slot',
        'description': 'Dumping SLOT information from DMI (SMBIOS)',
        'parser': parser
    }
