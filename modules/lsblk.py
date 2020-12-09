
import re
from sysinfo_lib import camelCase

def parser(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            entry = {}
            kv = re.findall(r'(\S[^=]+)=\"([^"]*)\"', line)
            if kv:
                for pair in kv:
                    entry[camelCase(pair[0])] = pair[1].strip()

            if 'name' in entry:
                output[entry['name']] = entry

    return {'output': output}

def register(main):
    main['lsblk'] = {
        'cmd': 'lsblk -P -o NAME,KNAME,MAJ:MIN,FSTYPE,MOUNTPOINT,LABEL,UUID,PARTLABEL,PARTUUID,RA,RO,RM,MODEL,SERIAL,SIZE,STATE,OWNER,GROUP,MODE,ALIGNMENT,MIN-IO,OPT-IO,PHY-SEC,LOG-SEC,ROTA,SCHED,RQ-SIZE,TYPE,DISC-ALN,DISC-GRAN,DISC-MAX,DISC-ZERO,WSAME,WWN,RAND,PKNAME,HCTL,TRAN,REV,VENDOR',
        'description': 'Lists information about all block devices',
        'parser': parser
    }