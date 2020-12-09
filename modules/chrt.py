
import re

def parser(stdout, stderr):
    output = {}
    pid = None
    if stdout:
        for line in stdout.splitlines():
            pidSearch = re.search(r'^>>>\s+PID:\s+(\S+)', line)
            if pidSearch:
                pid = pidSearch.group(1)
                output[pid] = {'pid': pid, 'scheduling': {}, 'current': {}}

            if pid:
                sched = re.search(r'^SCHED_(\S+)[^:]+:\s*(\S+)', line)
                if sched:
                    output[pid]['scheduling'][sched.group(1).strip()] = sched.group(2).strip()

                current = re.search(r'current scheduling (\S+).*:\s*(\S+)', line)
                if current:
                    output[pid]['current'][current.group(1).strip()] = current.group(2).strip()
    return {'output': output}

def register(main):
    main['chrt'] = {
        'cmd': """ps -eo pid | grep -vi pid | xargs -I {} sh -c "echo '>>> PID: {}'; chrt -a --pid {}; echo '----'; chrt -m --pid {};" """,
        'description': 'Scheduling attributes of all the tasks (threads)',
        'parser': parser
    }
