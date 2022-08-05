from sysinfo_lib import parseTable, camelCase
import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    if stdout:
        output = parseTable(stdout, to_camelcase=to_camelcase)

    return {"output": output, "unprocessed": []}


def parser_detail(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        device = ""
        for line in stdout.splitlines():
            dev = re.search(r"^>>> Device: (\S+)", line)
            if dev:
                device = dev.group(1)
                output[device] = {}
                continue

            kv = re.search(r"^get (\w[^:]+): (.*)$", line)
            if kv:
                key = camelCase(kv.group(1), to_camelcase)
                value = kv.group(2)
                output[device][key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["blockdev"] = {
        "cmd": "blockdev --report | column -t",
        "description": "Block device ioctls",
        "parser": parser,
    }

    main["blockdev_detail"] = {
        "cmd": """blkid -o device | xargs -n 1 -I {} sh -c "echo '>>> Device: {}'; blockdev -v --getalignoff --getbsz --getdiscardzeroes --getfra --getiomin --getioopt --getmaxsect --getpbsz --getra --getro --getsize64 --getss {}" """,
        "description": "Block device ioctls details",
        "parser": parser_detail,
    }
