from sysinfo_lib import parseCharDelimitedTable, tableToDict


def parser(stdout, stderr, to_camelcase):
    columnsNames = [
        "username",
        "password",
        "lastPasswordChange",
        "minimum",
        "maximum",
        "warn",
        "inactive",
        "expire",
    ]
    output = parseCharDelimitedTable(stdout, ":", columnsNames)
    output = tableToDict(output, "username")

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "etc_shadow",
            "system": ["linux"],
            "cmd": "cat /etc/shadow",
            "description": "Shadow database of the passwd file",
            "parser": parser,
        }
    )
