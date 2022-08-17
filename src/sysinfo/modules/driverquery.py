import re
from sysinfo_lib import camelCase, fixMultilineAndSplit


def parser_fo(stdout, stderr, to_camelcase):
    output = []
    unprocessed = []
    image = {}

    if stdout:
        data = fixMultilineAndSplit(stdout, r"^\s+", ", ")

        for line in data:
            if line.strip() == "":
                continue

            kv = re.search(r"^([^:]+):\s*(.*)$", line)
            if kv:
                key = camelCase(kv.group(1).strip(), to_camelcase)
                value = kv.group(2).strip().replace("\u00a0", "")

                if (
                    key == "moduleName"
                    or key == "Module Name"
                    or key == "deviceName"
                    or key == "DeviceName"
                ):
                    image = {}
                    output.append(image)

                image[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):

    main.register(
        {
            "name": "driverquery",
            "system": ["windows"],
            "cmd": "%SystemRoot%\\system32\\driverquery.exe /v /fo list",
            "description": "List of installed device drivers.",
            "parser": parser_fo,
        }
    )

    main.register(
        {
            "name": "driverquery_signed",
            "system": ["windows"],
            "cmd": "%SystemRoot%\\system32\\driverquery.exe /si /fo list",
            "description": "List of installed device signed drivers.",
            "parser": parser_fo,
        }
    )
