
import re

def parser(stdout, stderr):
	output = ''
	if stdout:
		output = re.sub(r'\n|\r|\r\n', '', stdout)
		output = stdout.strip()

	return {'output': output}

def register(main):
	main['kernel_name'] = {
		'cmd': 'uname -s',
		'description': 'Kernel name',
		'parser': parser
	}

	main['kernel_release'] = {
		'cmd': 'uname -r',
		'description': 'Kernel release',
		'parser': parser
	}

	main['kernel_version'] = {
		'cmd': 'uname -v',
		'description': 'Kernel version',
		'parser': parser
	}

	main['nodename'] = {
		'cmd': 'uname -n',
		'description': 'Network node hostname',
		'parser': parser
	}

	main['machine'] = {
		'cmd': 'uname -m',
		'description': 'Machine hardware name',
		'parser': parser
	}

	main['processor'] = {
		'cmd': 'uname -p',
		'description': 'Processor type',
		'parser': parser
	}

	main['hardware_platform'] = {
		'cmd': 'uname -i',
		'description': 'Hardware platform',
		'parser': parser
	}

	main['operating_system'] = {
		'cmd': 'uname -o',
		'description': 'Operating system',
		'parser': parser
	}
