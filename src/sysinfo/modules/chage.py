import re
from sysinfo_lib import camelCase


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []
    user = None

    if stdout:
        for line in stdout.splitlines():
            user_match = re.search(r"^>>> User:\s+(.*)$", line)
            if user_match:
                user = user_match.group(1)
                output[user] = {"name": user}
                continue

            kv = re.search(r"^([^:]+):\s*(.*)$", line)
            if user and kv:
                key = camelCase(kv.group(1).strip(), to_camelcase)
                value = kv.group(2).strip()

                output[user][key] = value
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main.register(
        {
            "name": "chage",
            "system": ["linux"],
            "cmd": """cat /etc/passwd | awk '{split($0,a,":"); print a[1]}' | xargs -I {} sh -c "echo '>>> User: {}'; chage -l {}" """,
            "description": "Users password expiration information",
            "parser": parser,
        }
    )
