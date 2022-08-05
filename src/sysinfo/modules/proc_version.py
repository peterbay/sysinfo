def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = stdout.strip()

    return {"output": output, "unprocessed": []}


def register(main):
    main.register(
        {
            "name": "proc_version",
            "system": ["linux"],
            "cmd": "cat /proc/version",
            "description": "Version of the Linux kernel, the version of gcc used to compile the kernel, and the time of kernel compilation",
            "parser": parser,
        }
    )
