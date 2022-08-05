import re


def parse_mount_options(value):
    output = {}
    for option in re.split(r"\s*,\s*", value):
        dir = re.search(r"^([^=]+)=(.*)$", option)

        if dir:
            output[dir.group(1)] = dir.group(2).split(":")

        else:
            output[option] = True

    return output


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            values = re.split(r"\s+", line)
            if len(values) > 5:
                output[values[1]] = {
                    "partition": values[0],
                    "mountPoint": values[1],
                    "fileSystem": values[2],
                    "mountOptions": parse_mount_options(values[3]),
                    "dump": values[4],
                    "fsckOrder": values[5],
                }
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "etc_mtab",
            "system": ["linux"],
            "cmd": "cat /etc/mtab",
            "description": "Currently mounted filesystems",
            "parser": parser,
        }
    )
