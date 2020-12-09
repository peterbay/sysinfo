
from sysinfo_lib import parseTable

def parser(stdout, stderr):
    output = {}
    if stdout:
        output = parseTable(stdout, r'^(\s*NS)(\sTYPE\s+)(\sPATH\s*)(\s\s*NPROCS)(\s*\sPID)(\s*\sPPID)(\s*\sUID)(\sUSER\s*)(\sCOMMAND\s*)')

    return {'output': output}

def register(main):
    main['lsns'] = {
        'cmd': 'lsns -o NS,TYPE,PATH,NPROCS,PID,PPID,UID,USER,COMMAND',
        'description': 'Block device ioctls',
        'parser': parser
    }