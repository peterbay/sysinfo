import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        values = re.search(r"^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", stdout.strip())
        if values:
            output = {
                "periodLast": values.group(1),
                "period5minute": values.group(2),
                "period15minute": values.group(3),
                "processes": values.group(4),
                "lastPid": values.group(5),
            }

        else:
            unprocessed.append(stdout)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_loadavg",
            "system": ["linux"],
            "cmd": "cat /proc/loadavg",
            "description": "Load average in regard to both the CPU and IO over time",
            "parser": parser,
        }
    )
