import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    pid = None
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():

            pidSearch = re.search(r"^>>>\s+PID:\s+(\S+)", line)
            if pidSearch:
                pid = pidSearch.group(1)
                output[pid] = {"pid": pid, "scheduling": {}, "current": {}}
                continue

            if pid:
                sched = re.search(r"^SCHED_(\S+)[^:]+:\s*(\S+)", line)
                if sched:
                    key = camelCase(sched.group(1).strip(), to_camelcase)
                    value = sched.group(2).strip()

                    output[pid]["scheduling"][key] = value
                    continue

                current = re.search(r"current scheduling (\S+).*:\s*(\S+)", line)
                if current:
                    key = camelCase(current.group(1).strip(), to_camelcase)
                    value = current.group(2).strip()

                    if re.match(r"^SCHED_", value):
                        value = camelCase(value.replace("SCHED_", ""), to_camelcase)

                    output[pid]["current"][key] = value
                    continue

            if line.strip("-") == "":
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "chrt",
            "system": ["linux"],
            "cmd": """ps -eo pid | grep -vi pid | xargs -I {} sh -c "echo '>>> PID: {}'; chrt -a --pid {}; echo '----'; chrt -m --pid {};" """,
            "description": "Scheduling attributes of all the tasks (threads)",
            "parser": parser,
        }
    )
