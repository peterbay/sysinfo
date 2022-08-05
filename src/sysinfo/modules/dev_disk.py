import re


def parser(stdout, stderr, to_camelcase):
    output = {"all": {}}
    unprocessed = []

    if stdout:
        typeName = ""
        for line in stdout.splitlines():
            matchType = re.search(r"^\/dev\/disk\/by-(.*):\s*$", line)
            if matchType:
                typeName = matchType.group(1)
                output[typeName] = {}
                continue

            matchEntry = re.search(r"\s(\S+)\s+->\s+[\.\/]+(.*)$", line)
            if matchEntry and typeName:
                key = matchEntry.group(1).strip()
                value = matchEntry.group(2).strip()
                output[typeName][key] = value

                if not value in output["all"]:
                    output["all"][value] = {}

                output["all"][value][typeName] = key
                continue

            if line == "" or re.match(r"^total", line):
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["dev_disk"] = {
        "cmd": "ls -l /dev/disk/by-*",
        "description": "Disk devices mapping",
        "parser": parser,
    }
