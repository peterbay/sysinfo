from sysinfo_lib import parseTable


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseTable(
            stdout,
            header_pattern=r"^(Destination\s*)(\sGateway\s*)(\sGenmask\s*)(\sFlags\s*)(\sMetric\s*)(\sRef\s)(\s*Use)(\sIface\s*)(\sMSS\s*)(\sWindow\s*)(\sirtt\s*)",
            to_camelcase=to_camelcase,
        )

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "route",
            "system": ["linux"],
            "cmd": "route -ee",
            "description": "IP routing table",
            "parser": parser,
        }
    )
