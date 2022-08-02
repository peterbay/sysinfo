def parser(stdout, stderr, to_camelcase):
    output = ""

    if stdout:
        output = stdout.strip()

    return {"output": output, "unprocessed": []}


def register(main):
    main["etc_timezone"] = {
        "cmd": "cat /etc/timezone",
        "description": "Timezone settings",
        "parser": parser,
    }
