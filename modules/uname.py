import re


def parser(stdout, stderr, to_camelcase):
    output = ""

    if stdout:
        output = re.sub(r"\n|\r|\r\n", "", stdout)
        output = stdout.strip()

    return {"output": output, "unprocessed": []}


def register(main):
    main["kernel_name"] = {
        "cmd": "uname -s",
        "description": "Kernel name (uname)",
        "parser": parser,
    }

    main["kernel_release"] = {
        "cmd": "uname -r",
        "description": "Kernel release (uname)",
        "parser": parser,
    }

    main["kernel_version"] = {
        "cmd": "uname -v",
        "description": "Kernel version (uname)",
        "parser": parser,
    }

    main["nodename"] = {
        "cmd": "uname -n",
        "description": "Network node hostname (uname)",
        "parser": parser,
    }

    main["machine"] = {
        "cmd": "uname -m",
        "description": "Machine hardware name (uname)",
        "parser": parser,
    }

    main["processor"] = {
        "cmd": "uname -p",
        "description": "Processor type (uname)",
        "parser": parser,
    }

    main["hardware_platform"] = {
        "cmd": "uname -i",
        "description": "Hardware platform (uname)",
        "parser": parser,
    }

    main["operating_system"] = {
        "cmd": "uname -o",
        "description": "Operating system (uname)",
        "parser": parser,
    }
