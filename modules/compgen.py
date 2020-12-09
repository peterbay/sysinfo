
from sysinfo_lib import sortedList

def parser(stdout, stderr):
	if stdout:
		return {'output': sortedList(stdout)}
	else:
		return {}

def register(main):
	main['shell_alias'] = {
		'cmd': '$(which bash) -c "compgen -a"',
		'description': 'Shell alias names',
		'parser': parser
	}

	main['shell_builtins'] = {
		'cmd': '$(which bash) -c "compgen -b"',
		'description': 'Names of shell builtin commands',
		'parser': parser
	}

	main['shell_all_commands'] = {
		'cmd': '$(which bash) -c "compgen -c"',
		'description': 'Shell command names',
		'parser': parser
	}

	main['shell_exported_variables'] = {
		'cmd': '$(which bash) -c "compgen -e"',
		'description': 'Names of exported shell variables',
		'parser': parser
	}

	main['groups'] = {
		'cmd': '$(which bash) -c "compgen -g"',
		'description': 'Group names',
		'parser': parser
	}

	main['jobs'] = {
		'cmd': '$(which bash) -c "compgen -j"',
		'description': 'Job names, if job control is active',
		'parser': parser
	}

	main['services'] = {
		'cmd': '$(which bash) -c "compgen -s"',
		'description': 'Service names',
		'parser': parser
	}

	main['users'] = {
		'cmd': '$(which bash) -c "compgen -u"',
		'description': 'User names',
		'parser': parser
	}

	main['shell_variables'] = {
		'cmd': '$(which bash) -c "compgen -v"',
		'description': 'Names of all shell variables',
		'parser': parser
	}
