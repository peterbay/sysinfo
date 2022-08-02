import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            kv = re.search(r"^\s*([^:]+):\s*(.*)$", line)
            if kv:
                key = kv.group(1).strip()
                value = kv.group(2).strip()

                output[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_dma"] = {
        "cmd": "cat /proc/dma",
        "description": "List of the registered ISA DMA channels in use",
        "parser": parser,
    }
