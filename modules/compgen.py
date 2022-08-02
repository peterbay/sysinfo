from sysinfo_lib import sortedList


def parser(stdout, stderr, to_camelcase):
    if stdout:
        return {"output": sortedList(stdout), "unprocessed": []}

    else:
        return {}


def register(main):
    main["shell_alias"] = {
        "cmd": '$(which bash) -c "compgen -a"',
        "description": "Shell alias names (compgen)",
        "parser": parser,
    }

    main["shell_builtins"] = {
        "cmd": '$(which bash) -c "compgen -b"',
        "description": "Names of shell builtin commands (compgen)",
        "parser": parser,
    }

    main["shell_all_commands"] = {
        "cmd": '$(which bash) -c "compgen -c"',
        "description": "Shell command names (compgen)",
        "parser": parser,
    }

    main["shell_exported_variables"] = {
        "cmd": '$(which bash) -c "compgen -e"',
        "description": "Names of exported shell variables (compgen)",
        "parser": parser,
    }

    main["shell_variables"] = {
        "cmd": '$(which bash) -c "compgen -v"',
        "description": "Names of all shell variables (compgen)",
        "parser": parser,
    }

    main["groups"] = {
        "cmd": '$(which bash) -c "compgen -g"',
        "description": "Group names (compgen)",
        "parser": parser,
    }

    main["jobs"] = {
        "cmd": '$(which bash) -c "compgen -j"',
        "description": "Job names, if job control is active (compgen)",
        "parser": parser,
    }

    main["services"] = {
        "cmd": '$(which bash) -c "compgen -s"',
        "description": "Service names (compgen)",
        "parser": parser,
    }

    main["users"] = {
        "cmd": '$(which bash) -c "compgen -u"',
        "description": "User names (compgen)",
        "parser": parser,
    }
