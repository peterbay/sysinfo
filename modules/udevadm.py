
import re

def parser(stdout, stderr):
    output = {'devices': {}, 'parents': {}}
    types = {
        'P': 'path',
        'N': 'node',
        'L': 'linkPriority',
        'E': 'entry',
        'S': 'link'
    };
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
                        output['devices'][device]['entry'][valueSearch.group(1)] = valueSearch.group(2).strip()
                
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
                    output['parents'][parent][parentKeyValue.group(1)] = parentKeyValue.group(2)

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
