import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        reSplit = re.compile(r"\s+")
        for line in stdout.splitlines():
            cols = reSplit.split(line)
            if len(cols) > 11:
                if cols[11].lower() == "mounted":
                    continue

                output[cols[11]] = {
                    "source": cols[0],
                    "fstype": cols[1],
                    "itotal": cols[2],
                    "iused": cols[3],
                    "iavail": cols[4],
                    "ipcent": cols[5],
                    "size": cols[6],
                    "used": cols[7],
                    "avail": cols[8],
                    "pcent": cols[9],
                    "file": cols[10],
                    "target": cols[11],
                }
                continue

            if re.match(r"Filesystem", line):
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "df",
            "system": ["linux"],
            "cmd": "df -a --output=source,fstype,itotal,iused,iavail,ipcent,size,used,avail,pcent,file,target",
            "description": "Report file system disk space usage",
            "parser": parser,
        }
    )
