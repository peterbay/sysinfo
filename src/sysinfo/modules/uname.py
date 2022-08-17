import re


def parser(stdout, stderr, to_camelcase):
    output = ""

    if stdout:
        output = re.sub(r"\n|\r|\r\n", "", stdout)
        output = stdout.strip()

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "kernel_name",
            "system": ["linux"],
            "cmd": "uname -s",
            "description": "Kernel name (uname)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "kernel_release",
            "system": ["linux"],
            "cmd": "uname -r",
            "description": "Kernel release (uname)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "kernel_version",
            "system": ["linux"],
            "cmd": "uname -v",
            "description": "Kernel version (uname)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "nodename",
            "system": ["linux"],
            "cmd": "uname -n",
            "description": "Network node hostname (uname)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "machine",
            "system": ["linux"],
            "cmd": "uname -m",
            "description": "Machine hardware name (uname)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "processor",
            "system": ["linux"],
            "cmd": "uname -p",
            "description": "Processor type (uname)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "hardware_platform",
            "system": ["linux"],
            "cmd": "uname -i",
            "description": "Hardware platform (uname)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "operating_system",
            "system": ["linux"],
            "cmd": "uname -o",
            "description": "Operating system (uname)",
            "parser": parser,
        }
    )
