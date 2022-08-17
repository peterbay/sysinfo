import re


def parser(stdout, stderr, to_camelcase):
    output = []
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            entrySearch = re.search(
                r"^\s*([^-]+)-(\S+)\s*:\s*(.*)$", line, re.IGNORECASE
            )
            if entrySearch:
                output.append(
                    {
                        "from": entrySearch.group(1),
                        "to": entrySearch.group(2),
                        "device": entrySearch.group(3),
                    }
                )
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "proc_ioports",
            "system": ["linux"],
            "cmd": "cat /proc/ioports",
            "description": "List of currently registered port regions used for input or output communication with a device",
            "parser": parser,
        }
    )
