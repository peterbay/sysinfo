import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            lineSplit = re.split(r"[\s\t]+", line)
            if lineSplit and len(lineSplit) > 4:
                accessValues = {}
                for access in re.split(r",", lineSplit[3]):
                    accessSplit = re.split(r"=", access + "=")
                    accessValues[accessSplit[0]] = accessSplit[1]

                output[lineSplit[1]] = {
                    "device": lineSplit[0],
                    "mountPoint": lineSplit[1],
                    "type": lineSplit[2],
                    "access": accessValues,
                }
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_mounts"] = {
        "cmd": "cat /proc/mounts",
        "description": "List mounted filesystems (info provides from kernel)",
        "parser": parser,
    }
