
import re
import sys
from struct import pack, unpack
from sysinfo_lib import camelCase

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3 

def parser_stats(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            entry = re.search(r'^\s*(\d+)\s+(.*)$', line)
            if entry:
                output[camelCase(entry.group(2).strip())] = entry.group(1).strip()

    return {'output': output}

def parser_disk(stdout, stderr):
    output = {}
    sectionsNames = []
    sectionsMask = ''
    totalLength = 0
    columnPaths = []
    if stdout:
        for line in stdout.splitlines():
            if re.match(r'disk.*reads', line, re.IGNORECASE):
                topHeader = re.split(r'\s+', line)
                if topHeader:
                    for value in topHeader:
                        sectionsNames.append(value.strip().strip('-').lower())
                        totalLength += len(value) + 1
                        sectionsMask += str(len(value) + 1) + 's'

            elif not sectionsMask:
                continue

            if re.match(r'.*total.*merged.*sectors.*', line):
                lineFix = line + (' ' * (totalLength - len(line)))
                if sys.version_info[0] != 2:
                    lineFix = bytes(lineFix, 'utf-8')
                
                sectionData = unpack(sectionsMask, lineFix)
                if sectionData:
                    index = 0

                    for sec in sectionData:
                        if PY2:
                            secStrip = sec.strip()
                        else:
                            secStrip = str(sec.strip(), 'utf-8')

                        topColumns = re.split(r'\s+', secStrip)
                        if topColumns:

                            for column in topColumns:
                                if column:
                                    columnPaths.append(camelCase('%s %s' %(sectionsNames[index], column, )))
                                else:
                                    columnPaths.append('%s' %(sectionsNames[index], ))
                        index += 1
            else:
                entry = {}
                columns = re.split(r'\s+', line)
                for ci, cv in enumerate(columns):
                    if ci < len(columnPaths):
                        entry[columnPaths[ci]] = cv
                if 'disk' in entry:
                    output[entry['disk']] = entry

    return {'output': output}

def parser_disk_sum(stdout, stderr):
    output = {}
    if stdout:
        for line in stdout.splitlines():
            entry = re.search(r'^\s*(\d+)\s+(.*)$', line)
            if entry:
                output[camelCase(entry.group(2).strip())] = entry.group(1).strip()

    return {'output': output}

def parser_forks(stdout, stderr):
    output = {}
    if stdout:
        forks = re.search(r'\s*(\d+)\s*forks', stdout)
        if forks:
            output['forks'] = forks.group(1)

    return {'output': output}

def register(main):
    main['vmstat_stats'] = {
        'cmd': 'vmstat -s',
        'description': 'Displays a table of various event counters and memory statistics',
        'parser': parser_stats
    }

    main['vmstat_disk'] = {
        'cmd': 'vmstat -dwn',
        'description': 'Report disk statistics',
        'parser': parser_disk
    }

    main['vmstat_disk_sum'] = {
        'cmd': 'vmstat -D',
        'description': 'Report some summary statistics about disk activity',
        'parser': parser_disk_sum
    }

    main['vmstat_forks'] = {
        'cmd': 'vmstat -f',
        'description': 'Displays the number of forks since boot',
        'parser': parser_forks
    }
