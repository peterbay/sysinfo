
import re

def parser_repolist(stdout, stderr):
    output = {'repos': [], 'errors': []}
    insideTable = False
    col1 = None
    col2 = None
    if stdout:
        for line in stdout.splitlines():
            print (line)
            tableHeader = re.search(r'^(repo id\s+)(repo name\s+)status', line, re.IGNORECASE)

            if col1 and col2:
                tableRow = re.search(r'^(.{%s})(.{%s})(.*)$' % (col1, col2), line)

                if insideTable and tableRow:
                    output['repos'].append({
                        'repo': tableRow.group(1).strip(),
                        'repo_name': tableRow.group(2).strip(),
                        'status': tableRow.group(3).strip()
                    })
                    continue

            if tableHeader:
                insideTable = True
                col1 = len(tableHeader.group(1))
                col2 = len(tableHeader.group(2))

            else:
                insideTable = False

    if stderr:
        for line in stderr.splitlines():
            if re.search(r'http.*error .*', line, re.IGNORECASE):
                if not line in output['errors']:
                    output['errors'].append(line)

    return {'output': output}

def parser_installed(stdout, stderr):
    output = {'packages': [], 'errors': []}
    if stdout:
        for line in stdout.splitlines():
            package = re.search(r'^([\S\.]+)\.(\S+)\s+(\S+\.\S+)\s+(\S+.*)$', line)
            if package:
                output['packages'].append({
                    'name': package.group(1).strip(),
                    'arch': package.group(2).strip(),
                    'version': package.group(3).strip(),
                    'status': package.group(4).strip()
                })

    if stderr:
        for line in stderr.splitlines():
            if re.search(r'http.*error .*', line, re.IGNORECASE):
                if not line in output['errors']:
                    output['errors'].append(line)

    return {'output': output}

def register(main):
    main['dnf_repolist'] = {
        'cmd': 'dnf repolist --all',
        'description': 'DNF - defined repositories',
        'parser': parser_repolist
    }

    main['dnf_installed'] = {
        'cmd': 'dnf list installed',
        'description': 'DNF - list installed packages',
        'parser': parser_installed
    }
