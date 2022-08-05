import re
from sysinfo_lib import parseTable, tableToDict, camelCase


def parser_services(stdout, stderr, to_camelcase):
    output = parseTable(stdout, to_camelcase=to_camelcase)
    output = tableToDict(output, "unit")

    return {"output": output, "unprocessed": []}


def parser_services_params(stdout, stderr, to_camelcase):
    output = {}
    service = None
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            service_search = re.search(r"^>>>\s*Service:\s*(.*)$", line)
            if service_search:
                service = service_search.group(1).strip()
                output[service] = {}
                continue

            if service:
                kv = re.search(r"^([^=]+)=(.*)$", line)
                if kv:
                    key = camelCase(kv.group(1), to_camelcase)
                    value = kv.group(2).strip()

                    output[service][key] = value
                    continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "services_list",
            "system": ["linux"],
            "cmd": """systemctl -l --type service --all --plain | grep -i -e ".service\|description" | sed 's/^\s*//g' """,
            "description": "Displays services with status",
            "parser": parser_services,
        }
    )

    main.register(
        {
            "name": "services_params",
            "system": ["linux"],
            "cmd": """systemctl -l --type service --all --plain | sed -E 's/^\s*(\\S+.service).*$/\\1/g' | grep -i -e ".service" | xargs -I '{}' sh -c "echo '>>> Service: {}'; systemctl show {} --no-page" """,
            "description": "Displays services with params",
            "parser": parser_services_params,
        }
    )
