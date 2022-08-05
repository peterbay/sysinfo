from sysinfo_lib import parseSpaceTable


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseSpaceTable(stdout, to_camelcase=to_camelcase)

    return {"output": output, "unprocessed": []}


def register(main):
    main["proc_swaps"] = {
        "cmd": "cat /proc/swaps",
        "description": "Measures swap space and its utilization",
        "parser": parser,
    }
