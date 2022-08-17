from sysinfo_lib import parseTable
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
    if stdout:
        output = parseTable(stdout, to_camelcase=to_camelcase)

    for entry in output:
        if "options" in entry:
            entry["options"] = parse_mount_options(entry["options"])

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "findmnt",
            "system": ["linux"],
            "cmd": "findmnt -Al | column -t",
            "description": "List all mounted filesytems",
            "parser": parser,
        }
    )
