import re


def parser(stdout, stderr, to_camelcase):
    output = {"all": {}}
    unprocessed = []

    if stdout:
        typeName = ""
        for line in stdout.splitlines():
            matchType = re.search(r"^\/dev\/input\/by-(.*):\s*$", line)
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
    main.register(
        {
            "name": "dev_input",
            "system": ["linux"],
            "cmd": "ls -l /dev/input/by-*",
            "description": "Input devices mapping",
            "parser": parser,
        }
    )
