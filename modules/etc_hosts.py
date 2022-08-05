import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            values = re.search(r"^\/etc\/([^\:]+):\s*(.*)$", line)
            if values:
                group = values.group(1)
                value = values.group(2).strip()

                if value == "":
                    continue

                if re.match(r"\s*#", value):
                    # ignore line with comment
                    continue

                if group not in output:
                    output[group] = []

                if group in ["hosts"]:
                    parts = re.search(r"^(\S+)\s+([^#]+)#?(.*)$", value)
                    if parts:
                        ip = parts.group(1).strip()
                        hostnames = parts.group(2).strip()
                        comment = parts.group(3).strip()

                        output[group].append(
                            {
                                "ip": ip,
                                "hostnames": re.split(r"\s+", hostnames),
                                "comment": comment,
                            }
                        )
                        continue

                if group in ["hosts.allow", "hosts.deny"]:
                    print("value", value)
                    parts = re.search(r"^([^:]+):\s*([^:]+):?([^#]+)#?(.*)$", value)
                    if parts:
                        daemon_list = parts.group(1).strip().split(",")
                        client_list = parts.group(2).strip().split(",")
                        command = parts.group(3).strip()
                        comment = parts.group(4).strip()

                        output[group].append(
                            {
                                "daemonList": daemon_list,
                                "clientList": client_list,
                                "command": command,
                                "comment": comment,
                            }
                        )
                        continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["etc_hosts"] = {
        "cmd": """grep "" /etc/hosts*""",
        "description": "Maps hostnames to IP addresses",
        "parser": parser,
    }
