import platform

from modules.sysinfo_lib import camelCase


try:
    import pkg_resources

    loaded_pkg_resources = True
except:
    loaded_pkg_resources = False


def python_pip_packages(to_camelcase):
    output = {}

    if loaded_pkg_resources:
        for pkg in pkg_resources.working_set:
            package = {}
            for key in [
                "location",
                "project_name",
                "key",
                "version",
                "parsed_version",
                "py_version",
                "platform",
                "precedence",
            ]:
                if hasattr(pkg, key):
                    key_case = camelCase(key, to_camelcase)
                    package[key_case] = str(getattr(pkg, key))

            if "key" in package:
                output[package["key"]] = package

    return {"output": output, "unprocessed": []}


def python_platform(to_camelcase):
    output = {
        "architecture": platform.architecture(),
        "machine": platform.machine(),
        "node": platform.node(),
        "platform": {
            "normal": platform.platform(),
            "aliased": platform.platform(aliased=True),
            "terse": platform.platform(terse=True),
        },
        "processor": platform.processor(),
        "python": {
            "branch": platform.python_branch(),
            "build": platform.python_build(),
            "compiler": platform.python_compiler(),
            "implementation": platform.python_implementation(),
            "revision": platform.python_revision(),
            "version": platform.python_version(),
            "versionTuple": platform.python_version_tuple(),
        },
        "release": platform.release(),
        "system": platform.system(),
        "version": platform.version(),
        "uname": platform.uname(),
    }
    return {"output": output, "unprocessed": []}


def register(main):
    if loaded_pkg_resources:
        main["python_pip_packages"] = {
            "function": python_pip_packages,
            "description": "List available python modules",
        }

    main["python_platform"] = {
        "function": python_platform,
        "description": "Probe the underlying platform's hardware, operating system, and Python interpreter version information",
    }
