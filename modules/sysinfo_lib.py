import sys
import re
from struct import pack, unpack

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3 

def sortedList(st):
    values = list(set(st.splitlines()))
    values.sort()
    return values

def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    if len(output) == 1:
        return output.lower()
    elif len(output) > 1:
        return output[0].lower() + output[1:]
    else:
        return ''

def parseTable(input, headerPattern = None, endPattern = None, ignoreEmpty = True):
    output = []
    colNames = []
    colLengths = []
    header = None
    lines = input.splitlines()

    if len(lines) == 0:
        return output

    while len(lines) > 0 and lines[0].strip() == '':
        lines.pop(0)

    if headerPattern:
        while len(lines) > 0 and not re.search(headerPattern, lines[0], re.IGNORECASE):
            lines.pop(0)

        if len(lines) == 0:
            return output

        header = re.search(headerPattern, lines.pop(0), re.IGNORECASE)
        if header:
            header = header.groups()

    else:
        header = re.findall(r'(\S+\s*)', lines.pop(0), re.IGNORECASE)

    if header:
        for value in header:
            colNames.append(camelCase(value.strip()))
            colLengths.append(len(value))

    if len(colNames) > 0:
        colLengths[-1] = 1024
        totalLength = sum(colLengths)
        packTemplate = ''.join([str(s) + 's' for s in colLengths])

        for line in lines:
            if ignoreEmpty == True and line.strip() == '':
                continue
            row = {}
            if endPattern and re.match(endPattern, line):
                break
            if PY2:
                cols = unpack(packTemplate, line + (' ' * (totalLength - len(line))))
            else:
                cols = unpack(packTemplate, bytes(line + (' ' * (totalLength - len(line))), 'utf-8'))
            for num, val in enumerate(cols, start=0):
                if PY2:
                    row[colNames[num]] = val.strip()
                else:
                    row[colNames[num]] = str(val.strip(), 'utf-8')
            output.append(row)

    return output

def parseSpaceTable(input, ignoreEmpty = True):
    output = []
    colNames = []
    lines = input.splitlines()

    if len(lines) == 0:
        return output

    while len(lines) > 0 and lines[0].strip() == '':
        lines.pop(0)

    header = re.findall(r'(\S+[\s\t]*)', lines.pop(0), re.IGNORECASE)
    if header:
        for value in header:
            colNames.append(camelCase(value.strip()))

    if len(colNames) > 0:
        for line in lines:
            if ignoreEmpty == True and line.strip() == '':
                continue
            row = {}
            cols = re.split(r'\s+', line.strip())
            for num, val in enumerate(cols, start=0):
                if num < len(colNames):
                    row[colNames[num]] = val.strip()
            output.append(row)

    return output

def parseCharDelimitedTable(input, delimiter, columnsNames):
    output = []
    if input:
        columns = len(columnsNames) + 1
        for line in input.splitlines():
            values = re.split(re.escape(delimiter), line + (delimiter * columns))
            row = {}
            for num, val in enumerate(columnsNames, start=0):
                if num < columns and num < len(values):
                    row[val] = values[num]
            output.append(row)
    return output

def tableToDict(input, key):
    output = {}

    for row in input:
        if isinstance(row, dict):
            if key in row:
                output[row[key]] = row
            else:
                return input
    
    return output
