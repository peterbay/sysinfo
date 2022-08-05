import re
from sysinfo_lib import camelCase


def extractDescriptors(data, lineNumber, offset, to_camelcase):
    output = {}
    ln = lineNumber
    descOffset = 0

    while ln < len(data):
        line = data[ln]

        searchOffset = re.search(r"^(\s*)", line)
        if searchOffset:
            lineOffset = len(searchOffset.group(1))

        if lineOffset < offset:
            ln -= 1
            break

        searchDesc = re.search(r"^(\s*)(.*Descriptor):\s*$", line, re.IGNORECASE)
        if searchDesc:
            descOffset = len(searchDesc.group(1)) + 2
            desc, ln = extractDescriptors(data, ln + 1, descOffset, to_camelcase)
            name = camelCase(searchDesc.group(2).strip(), to_camelcase)
            output[name] = desc
            ln += 1
            continue

        searchStatus = re.search(r"^(\s*)(.*Status):\s*(.*)$", line, re.IGNORECASE)
        if searchStatus:
            statusOffset = len(searchStatus.group(1)) + 2
            desc, ln = extractDescriptors(data, ln + 1, statusOffset, to_camelcase)
            name = camelCase(searchStatus.group(2).strip(), to_camelcase)
            if searchStatus.group(3).strip() != "":
                desc["value"] = searchStatus.group(3).strip()

            if name == "hubPortStatus":
                print("desc", desc)
            output[name] = desc
            ln += 1
            continue

        searchKeyIndexValue = re.search(r"^\s*(\S+)\s+([0-9]+):\s+(.*)$", line)
        if searchKeyIndexValue:
            key = camelCase(searchKeyIndexValue.group(1), to_camelcase)
            number = searchKeyIndexValue.group(2)
            value = searchKeyIndexValue.group(3).strip()

            valueSplit = re.search(r"^(\S+)\s+(\S.*)$", value)
            if valueSplit:
                value = [valueSplit.group(1), valueSplit.group(2)]

            if not key in output:
                output[key] = {}

            output[key][number] = value

            ln += 1
            continue

        searchKeyValue = re.search(r"^\s*(\S+)\s+([0-9].*)$", line)
        if searchKeyValue:
            key = camelCase(searchKeyValue.group(1).strip(":"), to_camelcase)
            value = searchKeyValue.group(2).strip()

            valueSplit = re.search(r"^(\S+)\s+(\S.*)$", value)
            if valueSplit:
                value = [valueSplit.group(1), valueSplit.group(2)]

            if key in output:
                output[key] = [output[key], value]
            else:
                output[key] = value

            ln += 1
            continue

        if not "data" in output:
            output["data"] = []

        output["data"].append(line.strip())

        ln += 1
    return output, ln


def parseBlock(data, to_camelcase):
    output = {}
    lines = data.split("\n")

    while lines[0].strip() == "":
        lines.pop(0)

    firstLine = lines.pop(0)
    busDevice = re.search(
        r"Bus\s+(\S+)\s+Device\s+([^:]+):\s+ID\s+([^:]+):(\S+)\s*(.*)$",
        firstLine,
        re.IGNORECASE,
    )
    if busDevice:
        output["bus"] = busDevice.group(1)
        output["device"] = busDevice.group(2)
        output["idVendor"] = busDevice.group(3)
        output["idProduct"] = busDevice.group(4)
        output["vendorProduct"] = busDevice.group(5)

    output["desc"], tmp = extractDescriptors(lines, 0, 0, to_camelcase)

    return output


def parser(stdout, stderr, to_camelcase):
    output = {}

    if stdout:
        delimiter = "-" * 20
        blocks = re.split(
            delimiter, re.sub(r"\n\nBus", "\n\n" + delimiter + "Bus", stdout)
        )
        if blocks:
            for block in blocks:
                blockData = parseBlock(block, to_camelcase)
                if "bus" in blockData and "device" in blockData:
                    id = blockData["bus"] + "/" + blockData["device"]
                    output[id] = blockData

    return {"output": output, "unprocessed": []}


def register(main):
    main["lsusb"] = {
        "cmd": "lsusb -v",
        "description": "List USB devices",
        "parser": parser,
    }
