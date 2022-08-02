import re


def parser(stdout, stderr, to_camelcase):
    output = {}
    modeName = ""
    unprocessed = []

    if stdout:
        for line in stdout.splitlines():
            mode = re.search(r'^\s*mode "([^"]+)\s*"$', line)
            if mode:
                modeName = mode.group(1)
                output[modeName] = {}
                continue

            endmode = re.search(r"^\s*endmode", line)
            if endmode:
                modeName = ""
                continue

            if modeName:
                geometry = re.search(
                    r"^\s+geometry\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*$", line
                )
                if geometry:
                    output[modeName]["geometry"] = {
                        "xres": geometry.group(1),
                        "yres": geometry.group(2),
                        "xresVirtual": geometry.group(3),
                        "yresVirtual": geometry.group(4),
                        "bitsPerPixel": geometry.group(5),
                    }
                    continue

                timings = re.search(
                    r"^\s+timings\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*$",
                    line,
                )
                if timings:
                    output[modeName]["timings"] = {
                        "pixclock": timings.group(1),
                        "leftMargin": timings.group(2),
                        "rightMargin": timings.group(3),
                        "upperMargin": timings.group(4),
                        "lowerMargin": timings.group(5),
                        "hsyncLen": timings.group(6),
                        "vsyncLen": timings.group(7),
                    }
                    continue

                rgba = re.search(
                    r"^\s+rgba\s*(\d+)\/(\d+),(\d+)\/(\d+),(\d+)\/(\d+),(\d+)\/(\d+)\s*$",
                    line,
                )
                if rgba:
                    output[modeName]["rgba"] = {
                        "redLength": rgba.group(1),
                        "redOffset": rgba.group(2),
                        "greenLength": rgba.group(3),
                        "greenOffset": rgba.group(4),
                        "blueLength": rgba.group(5),
                        "blueOffset": rgba.group(6),
                        "transpLength": rgba.group(7),
                        "transpOffset": rgba.group(8),
                    }
                    continue

                state = re.search(
                    r"^\s+(interlaced|double|vsync|hsync|csync|extsync)\s+(\S+)\s*$",
                    line,
                )
                if state:
                    output[modeName][state.group(1)] = state.group(2)
                    continue

                kv = re.search(r"^\s+(\S+)\s+(.*)$", line)
                if kv:
                    output[modeName][kv.group(1)] = kv.group(2)
                    continue

                unprocessed.append(line)

    return {"output": output, "unprocessed": unprocessed}


def parserInfo(stdout, stderr, to_camelcase):
    output = parser(stdout, stderr, to_camelcase)
    output["output"]["info"] = {}

    informationBlock = False
    if stdout:
        for line in stdout.splitlines():
            info = re.search(r"^\s*Frame buffer device information:\s*$", line)
            if info:
                informationBlock = True
                continue

            if informationBlock:
                keyValue = re.search(r"^\s+(\S+)\s*:\s+(.*)\s*$", line)
                if keyValue:
                    output["output"]["info"][keyValue.group(1)] = keyValue.group(2)
                    continue

    return output


def register(main):
    main["fbset"] = {
        "cmd": "fbset -a",
        "description": "Show frame buffer device settings",
        "parser": parser,
    }

    main["fbset_info"] = {
        "cmd": "fbset -i",
        "description": "Show frame buffer device information",
        "parser": parserInfo,
    }
