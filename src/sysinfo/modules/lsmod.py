import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            if re.match(r"Module.*Size", line):
                continue

            lineMatch = re.search(r"^(^\S+)\s*(\d+)\s*(\d+)\s*(.*)$", line)
            if lineMatch:
                used_by = lineMatch.group(4).split(",")
                if len(used_by) == 1:
                    if used_by[0] == "":
                        used_by = []

                output[lineMatch.group(1)] = {
                    "module": lineMatch.group(1),
                    "size": lineMatch.group(2),
                    "usedNumber": lineMatch.group(3),
                    "usedBy": used_by,
                }
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "lsmod",
            "system": ["linux"],
            "cmd": "lsmod",
            "description": "Show the status of modules in the Linux Kernel",
            "parser": parser,
        }
    )
