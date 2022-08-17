import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            if re.match(r"^\s*#", line):
                continue

            lineMatch = re.split(r"\s+", line)
            if lineMatch and len(lineMatch) > 5:
                output[lineMatch[0]] = {
                    "location": lineMatch[0],
                    "mountPoint": lineMatch[1],
                    "type": lineMatch[2],
                    "security": lineMatch[3],
                    "dump": lineMatch[4],
                    "fsckOrder": lineMatch[5],
                }
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "etc_fstab",
            "system": ["linux"],
            "cmd": "cat /etc/fstab",
            "description": "Filesystems mounted on boot",
            "parser": parser,
        }
    )
