from sysinfo_lib import parseSpaceTable, tableToDict


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        stdout = stdout.replace("#subsys_name", "subsys_name")

        output = parseSpaceTable(stdout, to_camelcase=to_camelcase)
        if to_camelcase:
            output = tableToDict(output, "subsysName")
        else:
            output = tableToDict(output, "subsys_name")

    return {"output": output, "unprocessed": []}


def register(main):
    main["proc_cgroups"] = {
        "cmd": "cat /proc/cgroups",
        "description": "Control  groups",
        "parser": parser,
    }
