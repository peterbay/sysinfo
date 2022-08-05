"""
 *
 * sysinfo - Python based scripts for obtaining system information from Linux.
 * 
 * Petr Vavrin (peterbay)   pvavrin@gmail.com
 *                          https://github.com/peterbay
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
"""

import os
import sys
import glob
import json
import argparse
import subprocess
from threading import Timer
from multiprocessing import Pool
from os.path import dirname, basename, isfile, join

sys.path.append(join(dirname(__file__), "modules"))

siModules = {}
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def loadModules():
    global siModules
    global PY2
    global PY3
    modules = glob.glob(join(dirname(__file__), "modules", "*.py"))
    for f in modules:
        if isfile(f) and not f.endswith("__init__.py"):
            if PY2:
                import imp

                lib = imp.load_source(basename(f)[:-3], f)
                if hasattr(lib, "register"):
                    lib.register(siModules)
            else:
                from importlib import import_module

                lib = __import__(basename(f)[:-3])
                if hasattr(lib, "register"):
                    lib.register(siModules)


def readFile(pathToFile):
    try:
        f = open(pathToFile, "r")
        content = f.read()
        f.close()
        return content, None

    except Exception as err:
        return None, err


def writeToFile(pathToFile, content):
    try:
        f = open(pathToFile, "w")
        f.write(content)
        f.close()

    except Exception as err:
        sys.stdout.write("ERROR: Can't write to file '%s': %s\n" % (pathToFile, err))


def pathCheck(args):
    if args.export_dir:
        if not os.access(args.export_dir, os.W_OK):
            sys.stdout.write(
                "ERROR: Export directory '%s' not exist or is not writable\n"
                % (args.export_dir,)
            )
            exit(1)

    if args.import_dir:
        if not os.access(args.import_dir, os.R_OK):
            sys.stdout.write(
                "ERROR: Import directory '%s' not exist or is not readable\n"
                % (args.import_dir,)
            )
            exit(1)


def kill(process):
    return process.kill()


def executeCmd(cmd):
    try:
        command = cmd.get("cmd", None)
        if not command:
            cmd["error"] = "Empty command"
            return

        proc = subprocess.Popen(
            command,
            shell=True,
            executable="/usr/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        cmdTimer = Timer(int(cmd.get("timeout", 30)), kill, [proc])

        try:
            cmdTimer.start()
            outs, errs = proc.communicate()

        except Exception as err:
            print(err)
            proc.kill()
            outs, errs = proc.communicate()
            cmd["error"] = err

        finally:
            cmdTimer.cancel()

    except Exception as err:
        print(err)
        cmd["error"] = err

    if proc:
        procPoll = proc.poll()
        if procPoll != 0:
            cmd["rc"] = procPoll
            if not "error" in cmd:
                cmd["error"] = "Unknown error"

    if PY2:
        cmd["stdout"] = outs
        cmd["stderr"] = errs
    else:
        cmd["stdout"] = str(outs, "utf-8")
        cmd["stderr"] = str(errs, "utf-8")


def execute(cmd):
    if not isinstance(cmd, dict):
        return {}

    if "import_dir" in cmd:
        commandImportPath = join(cmd.get("import_dir", ""), cmd.get("name", ""))
        cmd["stdout"], cmd["stderr"] = readFile(commandImportPath)

    else:
        outs, errs = "", ""
        to_camelcase = cmd.get("to_camelcase", None)

        if "function" in cmd:
            moduleFunction = cmd.get("function", None)
            if moduleFunction and callable(moduleFunction):
                outs = moduleFunction(to_camelcase)

            cmd["stdout"] = outs
            cmd["stderr"] = errs
            return cmd

        elif "cmd" in cmd:
            executeCmd(cmd)

    return cmd


def run(args):
    poolSize = int(args.pool)
    loadModules()
    p = Pool(poolSize)
    selectedModules = []
    executeModules = False
    results = {}

    to_camelcase = args.camel_case

    for name, settings in sorted(siModules.items()):
        if args.list:
            sys.stdout.write(
                "%-25s - %s\n"
                % (
                    name,
                    settings.get("description", ""),
                )
            )

        elif args.info:
            if "function" in settings:
                info = "built-in function"
            else:
                info = settings.get("cmd", "")

            sys.stdout.write(
                "%-25s - %s\n"
                % (
                    name,
                    info,
                )
            )

        elif args.all or name in args.commands:
            settings["name"] = name
            if args.import_dir:
                settings["import_dir"] = args.import_dir

            settings["to_camelcase"] = args.camel_case
            selectedModules.append(settings)
            executeModules = True

    if executeModules:
        for result in p.map(execute, selectedModules):
            name = result.get("name", None)
            if not name:
                continue

            if args.error and not result.get("error", None):
                continue

            if args.export_dir:
                commandExportPath = join(args.export_dir, name)
                writeToFile(commandExportPath, result.get("stdout", None))

            if args.export_only:
                continue

            parser = result.get("parser", None)
            if parser and callable(parser):
                try:
                    parsed = parser(
                        result.get("stdout", None),
                        result.get("stderr", None),
                        to_camelcase,
                    )

                    if isinstance(parsed, dict):
                        result["output"] = parsed.get("output", None)
                        result["unprocessed"] = parsed.get("unprocessed", None)

                except Exception as err:
                    result["parser_error"] = str(err)

            else:
                stdout = result.get("stdout", None)
                if isinstance(stdout, dict):
                    result["output"] = stdout.get("output", None)
                    result["unprocessed"] = stdout.get("unprocessed", None)

                else:
                    result["output"] = stdout
                    result["unprocessed"] = []

            result.pop("parser", None)
            result.pop("function", None)

            if not args.verbose and not args.error:
                result.pop("stdout", None)
                result.pop("stderr", None)
                result.pop("rc", None)
                result.pop("cmd", None)
                result.pop("description", None)
                result.pop("name", None)
                result.pop("unprocessed", None)
                result.pop("import_dir", None)

            results[name] = result

        if not args.export_only:
            if args.output:
                writeToFile(args.output, json.dumps(results, indent=4, sort_keys=True))

            else:
                sys.stdout.write(json.dumps(results, indent=4, sort_keys=True) + "\n")

    elif not args.list and not args.info:
        sys.stdout.write("No commands to execute\n")


def argsError(error):
    pass


def main(argv):
    parser = argparse.ArgumentParser()
    parser.error = argsError

    parser.add_argument(
        "--all", "-a", action="store_true", default=False, help="Execute all commands."
    )

    parser.add_argument(
        "--camel-case",
        "-c",
        action="store_true",
        default=False,
        help="Convert keys to CamelCase.",
    )

    parser.add_argument(
        "--error",
        "-e",
        action="store_true",
        default=False,
        help="Show only error outputs from commands.",
    )

    parser.add_argument(
        "--export-only",
        action="store_true",
        default=False,
        help="Export output from commands without processing.",
    )

    parser.add_argument(
        "--export-dir", help="Path to the directory for saving output from commands."
    )

    parser.add_argument(
        "--import-dir",
        help="Path to the directory for reading the stored outputs of commands.",
    )

    parser.add_argument(
        "--info",
        "-i",
        action="store_true",
        default=False,
        help="List all commands with command line arguments.",
    )

    parser.add_argument(
        "--list", "-l", action="store_true", default=False, help="List all commands."
    )

    parser.add_argument("--output", "-o", help="Path to the output file.")

    parser.add_argument(
        "--pool",
        "-p",
        default="5",
        type=int,
        help="Pool size for parallel execution of commands. (default value is 5)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Add more info to output - options, commands, raw command result.",
    )

    parser.add_argument("commands", nargs="*", help="Commands")

    args = parser.parse_args()
    pathCheck(args)
    run(args)


if __name__ == "__main__":
    main(sys.argv)
