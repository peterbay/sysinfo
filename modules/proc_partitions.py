from sysinfo_lib import parseSpaceTable, tableToDict


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseSpaceTable(stdout, to_camelcase=to_camelcase)
        output = tableToDict(output, "name")

    return {"output": output, "unprocessed": []}


def register(main):
    main["proc_partitions"] = {
        "cmd": "cat /proc/partitions",
        "description": "Partition block allocation information",
        "parser": parser,
    }
