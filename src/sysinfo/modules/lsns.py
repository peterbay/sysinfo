from sysinfo_lib import parseTable


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        output = parseTable(
            stdout,
            header_pattern=r"^(\s*NS)(\sTYPE\s+)(\sPATH\s*)(\s\s*NPROCS)(\s*\sPID)(\s*\sPPID)(\s*\sUID)(\sUSER\s*)(\sCOMMAND\s*)",
            to_camelcase=to_camelcase,
        )

    return {"output": output, "unprocessed": []}


def register(main):
    main["lsns"] = {
        "cmd": "lsns -o NS,TYPE,PATH,NPROCS,PID,PPID,UID,USER,COMMAND",
        "description": "Block device ioctls",
        "parser": parser,
    }
