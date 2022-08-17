import re


def parser(stdout, stderr, to_camelcase):
    output = []
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r"^(\S+)\s+(.*)\s+(\S+)$", line)
            if lineMatch:
                output.append(
                    {
                        "name": lineMatch.group(1).strip(),
                        "mode": lineMatch.group(2).strip(),
                        "link": lineMatch.group(3).strip(),
                    }
                )
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "update_alternatives",
            "system": ["linux"],
            "cmd": "update-alternatives --get-selections",
            "description": "Symbolic links determining default commands",
            "parser": parser,
        }
    )
