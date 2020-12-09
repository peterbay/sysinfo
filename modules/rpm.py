
from sysinfo_lib import parseCharDelimitedTable, tableToDict

def parser(stdout, stderr):
    output = {}
    columns = ['installtime', 'buildtime', 'name', 'version', 'release', 'arch', 'vendor', 'packager', 'distribution', 'disttag']
    if stdout:
        output = parseCharDelimitedTable(stdout, '|', columns)
        output = tableToDict(output, 'name')

    return {'output': output}

def register(main):
    main['rpm'] = {
        'cmd': 'rpm -q -a --queryformat "%{INSTALLTIME}|%{BUILDTIME}|%{NAME}|%{VERSION}|%{RELEASE}|%{arch}|%{VENDOR}|%{PACKAGER}|%{DISTRIBUTION}|%{DISTTAG}\n"',
        'description': 'Querying all RPM packages',
        'parser': parser
    }
