import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            kv = re.search(r"^(\S+)\s+(\S+)", line)
            if kv:
                key = kv.group(2).strip()
                value = kv.group(1).strip()

                output[key] = value
                continue

            k = re.search(r"^\s+(\S+)$", line)
            if k:
                output[k.group(1).strip()] = ""
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_filesystems"] = {
        "cmd": "cat /proc/filesystems",
        "description": "List of the file system types currently supported by the kernel",
        "parser": parser,
    }
