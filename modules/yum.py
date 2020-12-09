
import re

def parser_repolist(stdout, stderr):
    output = {'mirrors': [], 'repos': [], 'errors': []}
    insideTable = False
    if stdout:
        for line in stdout.splitlines():
            mirrors = re.search(r'^\s*\*\s*([^:]+):\s*(.*)$', line)
            if mirrors:
                output['mirrors'].append({
                    'repo': mirrors.group(1).strip(),
                    'host': mirrors.group(2).strip()
                })

            tableHeader = re.search(r'^repo id\s+repo name\s+status', line, re.IGNORECASE)
            tableRow = re.search(r'^([^\/]+)\/([^\/]+)\/(.*)\s\s+(\S+.*)\s\s+(\S+.*)$', line)
            if tableHeader:
                insideTable = True
            
            elif insideTable and tableRow:
                output['repos'].append({
                    'repo': tableRow.group(1).strip(),
                    'version': tableRow.group(2).strip(),
                    'arch': tableRow.group(3).strip(),
                    'repo_name': tableRow.group(4).strip(),
                    'status': tableRow.group(5).strip()
                })

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
    main['yum_repolist'] = {
        'cmd': 'yum repolist all',
        'description': 'YUM - defined repositories',
        'parser': parser_repolist
    }

    main['yum_installed'] = {
        'cmd': 'yum list installed',
        'description': 'YUM - list installed packages',
        'parser': parser_installed
    }
