
import re

def parser(stdout, stderr):
    output = {}
    columnsNames = [
        'user',
        'ruser',
        'group',
        'rgroup',
        'pid',
        'ppid',
        'pgid',
        'cpu',
        'size',
        'bytes',
        'nice',
        'time',
        'stime',
        'tty',
        'args'
    ]
    columnsCount = len(columnsNames)
    if stdout:
        for line in stdout.splitlines():
            if re.search(r'ps --cols 2048 -eo', line) or re.search(r'USER.*RUSER.*GROUP', line):
                continue

            cols = re.split(r'\s+', line)
            if cols:
                entry = {}
                for num, val in enumerate(cols, start=0):
                    if num < columnsCount:
                        name = columnsNames[num]
                        entry[name] = val
                    elif 'args' in entry:
                        entry['args'] += ' ' + val

            if 'pid' in entry:
                output[entry['pid']] = entry

    return {'output': output}

def register(main):
    main['ps'] = {
        'cmd': 'ps --cols 2048 -eo user:80,ruser:80,group:80,rgroup:80,pid,ppid,pgid,pcpu,vsz,nice,etime,time,stime,tty,args 2>/dev/null',
        'description': 'Report a snapshot of the current processes',
        'parser': parser
    }


