import re


def parser(stdout, stderr, to_camelcase):
    output = []
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            values = re.search(r"^\s*([^-]+)-(\S+)\s*:\s*(.*)$", line)
            if values:
                output.append(
                    {
                        "from": values.group(1),
                        "to": values.group(2),
                        "device": values.group(3),
                    }
                )
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_iomem",
            "system": ["linux"],
            "cmd": "cat /proc/iomem",
            "description": """Map of the system's memory for each physical device""",
            "parser": parser,
        }
    )
