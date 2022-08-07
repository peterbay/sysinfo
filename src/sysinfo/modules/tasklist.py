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

                if key == "imageName" or key == "Image Name":
                    image = {}
                    output.append(image)

                if (
                    key == "modules"
                    or key == "Modules"
                    or key == "services"
                    or key == "Services"
                ):
                    value = value.split(", ")

                image[key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):

    main.register(
        {
            "name": "tasklist",
            "system": ["windows"],
            "cmd": "%SystemRoot%\\system32\\tasklist.exe /fo list",
            "description": "Get currently running processes",
            "parser": parser_fo,
        }
    )

    main.register(
        {
            "name": "tasklist_services",
            "system": ["windows"],
            "cmd": "%SystemRoot%\\system32\\tasklist.exe /svc /fo list",
            "description": "Get services hosted in each process",
            "parser": parser_fo,
        }
    )

    main.register(
        {
            "name": "tasklist_apps",
            "system": ["windows"],
            "cmd": "%SystemRoot%\\system32\\tasklist.exe /apps /fo list",
            "description": "Get services hosted in each process",
            "parser": parser_fo,
        }
    )

    main.register(
        {
            "name": "tasklist_modules",
            "system": ["windows"],
            "cmd": "%SystemRoot%\\system32\\tasklist.exe /m /fo list",
            "description": "Get modules loaded in each process",
            "parser": parser_fo,
        }
    )
