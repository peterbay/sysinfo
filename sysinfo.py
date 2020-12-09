
import os
import sys
import glob
import json
import argparse
import subprocess
from threading import Timer
from multiprocessing import Pool
from os.path import dirname, basename, isfile, join

sys.path.append(join(dirname(__file__), 'modules'))

siModules = {}
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3 

def loadModules():
    global siModules
    global PY2
    global PY3
    modules = glob.glob(join(dirname(__file__), 'modules', '*.py'))
    for f in modules:
        if isfile(f) and not f.endswith('__init__.py'):
            if PY2:
                import imp
                lib = imp.load_source(basename(f)[:-3], f)
                if hasattr(lib, 'register'):
                    lib.register(siModules)
            else:
                from importlib import import_module
                lib = __import__(basename(f)[:-3])
                if hasattr(lib, 'register'):
                    lib.register(siModules)

def kill(process):
    return process.kill()

def execute(cmd):
    if not isinstance(cmd, dict):
        return {}

    outs, errs = '', ''

    try:
        proc = subprocess.Popen(cmd.get('cmd', ''), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmdTimer = Timer(int(cmd.get('timeout', 30)), kill, [proc])

        try:
            cmdTimer.start()
            outs, errs = proc.communicate()

        except Exception as err:
            proc.kill()
            outs, errs = proc.communicate()
            cmd['error'] = err

        finally:
            cmdTimer.cancel()

    except Exception as err:
        cmd['error'] = err

    if proc:
        procPoll = proc.poll()
        if procPoll != 0:
            cmd['rc'] = procPoll
            if not cmd.get('error', None):
                cmd['error'] = 'error'

    if PY2:
        cmd['stdout'] = outs
        cmd['stderr'] = errs
    else:
        cmd['stdout'] = str(outs, 'utf-8')
        cmd['stderr'] = str(errs, 'utf-8')

    return cmd

def writeToOutput(pathToFile, content):
    try:
        f = open(pathToFile, 'w')
        f.write(content)
        f.close()
    except Exception as err:
        sys.stdout.write('ERROR: Can\'t write to file \'%s\': %s\n' % (pathToFile, err))

def run(args):
    poolSize = int(args.pool)
    loadModules()
    p = Pool(poolSize)
    selectedModules = []
    executeModules = False
    results = {}

    for name, settings in sorted(siModules.items()):
        if args.list:
            sys.stdout.write('%-25s - %s\n' % (name, settings.get('description', ''), ))
        
        elif args.info:
            sys.stdout.write('%-25s - %s\n' % (name, settings.get('cmd', ''), ))

        elif args.all or name in args.commands:
            settings['name'] = name
            selectedModules.append(settings)
            executeModules = True

    if executeModules:
        for result in p.map(execute, selectedModules):
            name = result.get('name', None)
            if not name:
                continue

            if args.error and not result.get('error', None):
                continue

            parser = result.get('parser', None)
            if parser and callable(parser):
                parsed = parser(result.get('stdout', None), result.get('stderr', None))

                if isinstance(parsed, dict):
                    result['output'] = parsed.get('output', None)
                    result['ignored'] = parsed.get('ignored', None)

            else:
                result['output'] = result.get('stdout', None)

            result.pop('parser', None)

            if not args.verbose and not args.error:
                result.pop('stdout', None)
                result.pop('stderr', None)
                result.pop('rc', None)
                result.pop('cmd', None)
                result.pop('description', None)
                result.pop('name', None)
                result.pop('ignored', None)

            results[name] = result

        if args.output:
            writeToOutput(args.output, json.dumps(results, indent=4, sort_keys=True))
        else:
            sys.stdout.write(json.dumps(results, indent=4, sort_keys=True) + '\n')

    else:
        sys.stdout.write('No commands to execute\n')

def argsError(error):
    pass

def main(argv):
    parser = argparse.ArgumentParser()
    parser.error = argsError

    parser.add_argument('--all', '-a', action='store_true', default=False, help='Execute all commands.')
    parser.add_argument('--error', '-e', action='store_true', default=False, help='Show only error outputs from commands.')
    parser.add_argument('--info', '-i', action='store_true', default=False, help='List all commands with command line arguments.')
    parser.add_argument('--list', '-l', action='store_true', default=False, help='List all commands.')
    parser.add_argument('--output', '-o', help='Path to the output file.')
    parser.add_argument('--pool', '-p', default='5', type=int, help='Pool size for parallel execution of commands. (default value is 5)')
    parser.add_argument('--verbose', '-v', action='store_true', default=False, help='Add more info to output - options, commands, raw command result.')
    parser.add_argument('commands', nargs='*', help='Commands')

    args = parser.parse_args()
    run (args)

if __name__ == '__main__':
    main(sys.argv)
