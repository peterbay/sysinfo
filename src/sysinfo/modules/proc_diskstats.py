import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    columnNames = [
        "majorNumber",
        "minorNumber",
        "deviceName",
        "readsCompletedSuccessfully",
        "readsMerged",
        "sectorsRead",
        "timeSpentReading",
        "writesCompleted",
        "writesMerged",
        "sectorsWritten",
        "timeSpentWriting",
        "IOsCurrentlyInProgress",
        "timeSpentDoingIOs",
        "weightedTimeSpentDoingIOs",
    ]
    lenColumnNames = len(columnNames)
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            line = line.strip()
            columns = re.split(r"\s+", line)
            if columns:
                output[columns[2]] = {}
                for num, val in enumerate(columns, start=0):
                    if num < lenColumnNames:
                        output[columns[2]][columnNames[num]] = val
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_diskstats"] = {
        "cmd": "cat /proc/diskstats",
        "description": "I/O statistics of block devices",
        "parser": parser,
    }
