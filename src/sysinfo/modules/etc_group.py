from sysinfo_lib import parseCharDelimitedTable, tableToDict


def parser(stdout, stderr, to_camelcase):
    columnsNames = ["groupName", "password", "gid", "groupList"]
    output = parseCharDelimitedTable(stdout, ":", columnsNames)
    output = tableToDict(output, "groupName")

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "etc_group",
            "system": ["linux"],
            "cmd": "cat /etc/group",
            "description": "Groups essential information",
            "parser": parser,
        }
    )
