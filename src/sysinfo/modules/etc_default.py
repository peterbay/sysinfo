import re


def setPathValue(data, path, value):
    pathRest = None
    pathParts = re.search(r"^([^\/]+)\/?(.*)$", path)
    if pathParts:
        path = pathParts.group(1)
        pathRest = pathParts.group(2)

    if not path in data:
        data[path] = {}

    if pathRest:
        setPathValue(data[path], pathRest, value)

    else:
        if isinstance(data[path], dict):
            data[path] = []
        data[path].append(value)


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            pathValue = re.search(r"^\/etc\/default\/([^:]+):(.*)$", line)
            if pathValue:
                path = pathValue.group(1)
                value = pathValue.group(2)
                if value.strip() == "":
                    continue

                if not re.search(r"^\s*#", value):
                    setPathValue(output, path, value)
                    continue

                if re.match(r"^\s*#", value):
                    # ignore line with comment
                    continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "etc_default",
            "system": ["linux"],
            "cmd": 'find /etc/default -type f -follow -print | xargs grep ""',
            "description": "Default configuration for programs",
            "parser": parser,
        }
    )
