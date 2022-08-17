import re


def parser(stdout, stderr, to_camelcase):
    output = ""

    if stdout:
        output = re.sub(r"\n|\r|\r\n", "", stdout)
        output = stdout.strip()

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "proc_version_signature",
            "system": ["linux"],
            "cmd": "cat /proc/version_signature",
            "description": "OS version signature",
            "parser": parser,
        }
    )
