
import re

def parser(stdout, stderr):
    output = {}
    path = None
    if stdout:
        for line in stdout.splitlines():
            hostSearch = re.search(r'^Host:\s+(\S+)\s+Channel:\s+(\S+)\s+Id:\s+(\S+)\s+Lun:\s+(\S+)$', line, re.IGNORECASE)
            if hostSearch:
                host = hostSearch.group(1)
                channel = hostSearch.group(2)
                id = hostSearch.group(3)
                lun = hostSearch.group(4)
                path = '%s:%s:%s:%s' % (host.replace('scsi', ''), channel, id, lun)
                output[path] = {
                    'host': host,
                    'channel': channel,
                    'id': id,
                    'lun': lun
                }

            if path:
                vendorSearch = re.search(r'^\s+Vendor:\s+(.*)\s+Model:\s+(.*)\s+Rev:\s+(.*)$', line, re.IGNORECASE)
                if vendorSearch:
                    output[path]['vendor'] = vendorSearch.group(1).strip()
                    output[path]['model'] = vendorSearch.group(2).strip()
                    output[path]['rev'] = vendorSearch.group(3).strip()

                typeSearch = re.search(r'^\s+Type:\s+(.*)\s+ANSI\s+SCSI\s+revision:\s+(.*)$', line, re.IGNORECASE)
                if typeSearch:
                    output[path]['type'] = typeSearch.group(1).strip()
                    output[path]['revision'] = typeSearch.group(2).strip()

    return {'output': output}

def register(main):
    main['proc_scsi'] = {
        'cmd': 'cat /proc/scsi/scsi',
        'description': 'List of every recognized SCSI device',
        'parser': parser
    }
