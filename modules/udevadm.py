
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {'devices': {}, 'parents': {}}
    types = {
        'P': 'path',
        'N': 'node',
        'L': 'linkPriority',
        'E': 'entry',
        'S': 'link'
    }
    device = None
    parent = None
    if stdout:
        for line in stdout.splitlines():
            deviceSearch = re.search(r'^>>> Device: (\S+)', line)
            if deviceSearch:
                device = deviceSearch.group(1)
                output['devices'][device] = {'parents': [], 'entry': {}, 'link': []}
                parent = None

            if not device:
                continue

            keyValue = re.search(r'^(\S):\s+(.*)$', line)
            if keyValue:
                key = keyValue.group(1)
                value = keyValue.group(2).strip()
                if key in types:
                    key = types[key]

                if key == 'entry':
                    valueSearch = re.search(r'^([^=]+)=(.*)$', value)
                    if valueSearch:
                        subkey = valueSearch.group(1).lower()
                        subvalue = valueSearch.group(2).strip()
                        output['devices'][device]['entry'][subkey] = subvalue
                
                elif key == 'link':
                    output['devices'][device]['link'].append(value)

                else:
                    output['devices'][device][key] = value

            deviceLook = re.search(r'^\s+looking at device \'([^\']+)', line)
            if deviceLook:
                parent = deviceLook.group(1)
                if not parent in output['parents']:
                    output['parents'][parent] = {}
                output['devices'][device]['parents'].append(parent)

            parentDeviceLook = re.search(r'^\s+looking at device \'([^\']+)', line)
            if parentDeviceLook:
                parent = parentDeviceLook.group(1)
                if not parent in output['parents']:
                    output['parents'][parent] = {}
                output['devices'][device]['parents'].append(parent)

            if parent:
                parentKeyValue = re.search(r'^\s+([^=]+)=="([^"]+)"', line)
                if parentKeyValue:
                    key = parentKeyValue.group(1).lower()
                    value = parentKeyValue.group(2)

                    multipleValues = re.match(r'^(\s+\d+)+$', value)
                    if multipleValues:
                        value = re.split(r'\s+', value.strip())

                    keyAttr = re.match(r'^(\S+){([^}]+)}', key, re.IGNORECASE)
                    if keyAttr:
                        attrType = keyAttr.group(1).lower()
                        if not attrType in output['parents'][parent]:
                            output['parents'][parent][attrType] = {}

                        attrKey = camelCase(keyAttr.group(2))
                        output['parents'][parent][attrType][attrKey] = value

                    else:
                        output['parents'][parent][key] = value

    return {'output': output}


def register(main):
    main['udevadm'] = {
        'cmd': """udevadm info --export-db | grep "DEVNAME" | cut -d "=" -f2 | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; udevadm info --query=all --name={}; udevadm info --attribute-walk --name={}" """,
        'description': 'Queries the udev database for device information stored in the udev database',
        'parser': parser
    }

    main['udevadm_block_devices'] = {
        'cmd': """find /dev/ -type b | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; udevadm info --query=all --name={}; udevadm info --attribute-walk --name={}" """,
        'description': 'Queries the udev database for block device information stored in the udev database',
        'parser': parser
    }
