import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            lineMatch = re.search(r"^([^=]+)=(.*)$", line)
            if lineMatch:
                output[lineMatch.group(1)] = lineMatch.group(2)
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["env"] = {
        "cmd": "env",
        "description": "Environment variables",
        "parser": parser,
    }
