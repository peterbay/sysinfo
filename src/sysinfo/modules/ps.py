import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []
    columnsNames = [
        "user",
        "ruser",
        "group",
        "rgroup",
        "pid",
        "ppid",
        "pgid",
        "cpu",
        "size",
        "bytes",
        "nice",
        "time",
        "stime",
        "tty",
        "args",
    ]
    columnsCount = len(columnsNames)

    if stdout:
        for line in stdout.splitlines():
            if re.search(r"ps --cols 12288 -eo", line) or re.search(
                r"USER.*RUSER.*GROUP", line
            ):
                continue

            cols = re.split(r"\s+", line)
            if cols:
                entry = {}
                for num, val in enumerate(cols, start=0):
                    if num < columnsCount:
                        name = columnsNames[num]
                        entry[name] = val

                    elif "args" in entry:
                        entry["args"] += " " + val

            if "pid" in entry:
                output[entry["pid"]] = entry
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["ps"] = {
        "cmd": "ps --cols 12288 -eo user:256,ruser:256,group:256,rgroup:256,pid,ppid,pgid,pcpu,vsz,nice,etime,time,stime,tty,args 2>/dev/null",
        "description": "Report a snapshot of the current processes",
        "parser": parser,
    }
