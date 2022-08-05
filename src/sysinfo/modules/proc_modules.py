import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            lineSplit = re.split(r"[\s\t]+", line)
            if lineSplit and len(lineSplit) > 5:
                output[lineSplit[0]] = {
                    "moduleName": lineSplit[0],
                    "moduleMemorySize": lineSplit[1],
                    "numInstancesLoaded": lineSplit[2],
                    "depends": lineSplit[3].strip(",").split(","),
                    "state": lineSplit[4],
                    "kernelMemoryOffset": lineSplit[5],
                }
                continue

            unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def register(main):
    main["proc_modules"] = {
        "cmd": "cat /proc/modules",
        "description": "List of all modules loaded into the kernel",
        "parser": parser,
    }
