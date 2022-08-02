import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    columns = None
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            if re.search(r"total\s+used", line, re.IGNORECASE):
                columns = re.split(r"\s+", line.strip())
                continue

            entrySearch = re.search(r"^([^:]+):\s+(.*)$", line)
            if columns and entrySearch:
                type = camelCase(entrySearch.group(1), to_camelcase)
                output[type] = {}
                for idx, value in enumerate(
                    re.split(r"\s+", entrySearch.group(2).strip())
                ):
                    if idx < len(columns):
                        key = camelCase(columns[idx], to_camelcase)
                        output[type][key] = value

                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["free"] = {
        "cmd": "free -b -l -w",
        "description": "Amount of free and used memory in the system",
        "parser": parser,
    }
