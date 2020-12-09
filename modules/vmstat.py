
import re
import sys
from struct import pack, unpack
from sysinfo_lib import camelCase

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
    sectionsColumns = [None, None, None, None, None, None, None]
    sectionsMask = ''
    totalLength = 0
    if stdout:
        for line in stdout.splitlines():
            if re.match(r'disk.*reads', line, re.IGNORECASE):
                topHeader = re.split(r'\s+', line)
                if topHeader:
                    for value in topHeader:
                        sectionsNames.append(value.strip().strip('-'))
                        totalLength += len(value) + 1
                        sectionsMask += str(len(value) + 1) + 's'
            else:
                lineFix = line + (' ' * (totalLength - len(line)))
                if sys.version_info[0] != 2:
                    lineFix = bytes(lineFix, 'utf-8')

                sectionData = unpack(sectionsMask, lineFix)

                disk = None
                for num, val in enumerate(sectionData, start=0):
                    section = val.strip()
                    sectionName = sectionsNames[num]
                    if num == 0 and len(section) > 0:
                        disk = section
                        output[disk] = {}
                    elif disk:
                        output[disk][sectionName] = {}

                    sectionSplit = re.split(r'\s+', section)

                    if re.match(r'\D', section, re.IGNORECASE):
                        sectionsColumns[num] = sectionSplit

                    elif sectionsColumns[num]:
                        for numSec, valSec in enumerate(sectionSplit, start=0):
                            if numSec < len(sectionsColumns[num]):
                                colName = sectionsColumns[num][numSec]
                                output[disk][sectionName][colName.lower()] = valSec.strip()

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
