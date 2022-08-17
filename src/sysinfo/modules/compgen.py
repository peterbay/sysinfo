from sysinfo_lib import sortedList


def parser(stdout, stderr, to_camelcase):
    if stdout:
        return {"output": sortedList(stdout), "unprocessed": []}

    else:
        return {}


def register(main):
    main.register(
        {
            "name": "shell_alias",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -a"',
            "description": "Shell alias names (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "shell_builtins",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -b"',
            "description": "Names of shell builtin commands (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "shell_all_commands",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -c"',
            "description": "Shell command names (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "shell_exported_variables",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -e"',
            "description": "Names of exported shell variables (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "shell_variables",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -v"',
            "description": "Names of all shell variables (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "groups",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -g"',
            "description": "Group names (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "jobs",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -j"',
            "description": "Job names, if job control is active (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "services",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -s"',
            "description": "Service names (compgen)",
            "parser": parser,
        }
    )

    main.register(
        {
            "name": "users",
            "system": ["linux"],
            "cmd": '$(which bash) -c "compgen -u"',
            "description": "User names (compgen)",
            "parser": parser,
        }
    )
