from sysinfo_lib import parseCharDelimitedTable, tableToDict


def parser(stdout, stderr, to_camelcase):
    columnsNames = ["username", "password", "uid", "gid", "idInfo", "homeDir", "shell"]
    output = parseCharDelimitedTable(stdout, ":", columnsNames)
    output = tableToDict(output, "username")
    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "etc_passwd",
            "system": ["linux"],
            "cmd": "cat /etc/passwd",
            "description": "Attributes of each user or account on a computer",
            "parser": parser,
        }
    )
