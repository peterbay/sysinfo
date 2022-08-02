import re

opField = {
    "a": "accessMode",
    "c": "commandName",
    "C": "structureShareCount",
    "d": "deviceCharacterCode",
    "D": "majorMinorDeviceNumber",
    "f": "fileDescriptor",
    "F": "structureAddress",
    "g": "processGroupId",
    "G": "flags",
    "i": "inodeNumber",
    "k": "linkCount",
    "K": "taskId",
    "l": "lockStatus",
    "L": "loginName",
    "m": "markerBetweenRepeatedOutput",
    "n": "name",
    "N": "nodeIdentifier",
    "o": "fileOffset",
    "p": "processId",
    "P": "protocolName",
    "r": "rawDeviceNumber",
    "R": "parentPid",
    "s": "fileSize",
    "S": "streamModuleAndDeviceNames",
    "t": "fileType",
    "T": "tcpTpiInfo",
    "u": "userId",
    "z": "zoneName",
    "Z": "selinuxSecurityContext",
}

tcptpiField = {
    "QR": "readQueueSize",
    "QS": "sendQueueSize",
    "SO": "socketOptionsAndValues",
    "SS": "socketStates",
    "ST": "connectionState",
    "TF": "tcpFlagsAndValues",
    "WR": "windowReadSize",
    "WW": "windowWriteSize",
}


def parseElements(elements):
    global opField
    global tcptpiField
    output = {}
    for el in elements:
        ident = el[0:1]
        content = el[1:].strip()

        identType = opField.get(ident, ident)
        if identType:
            if not identType in output:
                output[identType] = {}

            if ident == "T":
                fifc = (content + "=").split("=")
                fifcType = tcptpiField.get(fifc[0], fifc[0])

                output[identType][fifcType] = fifc[1]

            else:
                output[identType] = content

    return output


def parser(stdout, stderr, to_camelcase):
    output = {}
    pid = None

    if stdout:
        for line in re.split(r"\x00\n", stdout):
            line = re.sub(r"^[\s\x00]*", "", line)
            elements = re.split(r"\x00", line)
            if not elements:
                continue

            first = elements.pop(0)
            if first:
                ident = first[0:1]
                content = first[1:]

                if ident == "p":
                    pid = content
                    output[pid] = parseElements(elements)
                    output[pid]["pid"] = pid
                    output[pid]["files"] = []

                if pid and ident == "f":
                    output[pid]["files"].append(parseElements(elements))

    return {"output": output, "unprocessed": []}


def register(main):
    main["lsof"] = {
        "cmd": "lsof -F0",
        "description": "Information about files opened by processes",
        "parser": parser,
    }
