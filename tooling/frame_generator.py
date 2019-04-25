import re
import urllib.request
import datetime
from pathlib import Path

CLASS_REGEX = re.compile('(frame_.+?)\{(.+?)\}', re.IGNORECASE | re.MULTILINE | re.DOTALL)
ENUM_REGEX = re.compile('frame_id.?\{(.+?)\}', re.IGNORECASE | re.MULTILINE | re.DOTALL)

SOURCE_URL = "https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp"
SOURCE_ANCHOR = "/** #PythonAnchor# */"
BASE_PATH = Path(__file__).parent.parent

# The different format converters
TYPE_FORMATS = {
    'char': 'c',
    'int8_t': 'c',
    'signed char': 'b',
    'unsigned char': 'B',
    'uint8_t': 'B',
    '_Bool': '?',
    'bool': '?',
    'short': 'h',
    'int16_t': 'h',
    'unsigned short': 'H',
    'uint16_t': 'H',
    'int': 'i',
    'int32_t': 'i',
    'unsigned int': 'I',
    'uint32_t': 'I',
    'long': 'l',
    'int64_t': 'l',
    'unsigned long': 'L',
    'uint64_t': 'L',
    'long long': 'q',
    'unsigned long long': 'Q',
    'ssize_t': 'n',
    'size_t': 'N',
    'float': 'f',
    'double': 'd',
    'char[]': 's',
    'void*': 'P',
    'void *': 'P'
}

TYPE_SIZES = {
    'char': 1,
    'int8_t': 1,
    'signed char': 1,
    'unsigned char': 1,
    'uint8_t': 1,
    '_Bool': 1,
    'bool': 1,
    'short': 2,
    'int16_t': 2,
    'unsigned short': 2,
    'uint16_t': 2,
    'int': 4,
    'int32_t': 4,
    'unsigned int': 4,
    'uint32_t': 4,

    # Yes, 4!
    # GCC 8.2 ARM has sizeof(long) == 4, sizeof(long long) == 8
    'long': 4,
    'int64_t': 4,
    'unsigned long': 4,
    'uint64_t': 8,
    'long long': 8,
    'unsigned long long': 8,
    'ssize_t': 4,
    'size_t': 4,
    'float': 4,
    'double': 8,

    # Note: arrays need other exceptions
    'char[]': 4,

    # While included, void* should be avoided!
    'void*': 4,
    'void *': 4
}

CORRESPONDING_TYPES = {
    'char': str,
    'int8_t': int,
    'signed char': str,
    'unsigned char': str,
    'uint8_t': int,
    '_Bool': bool,
    'bool': bool,
    'short': int,
    'int16_t': int,
    'unsigned short': int,
    'uint16_t': int,
    'int': int,
    'int32_t': int,
    'unsigned int': int,
    'uint32_t': int,
    'long': int,
    'int64_t': int,
    'unsigned long': int,
    'uint64_t': int,
    'long long': int,
    'unsigned long long': int,
    'ssize_t': int,
    'size_t': int,
    'float': float,
    'double': float,

    # Note: arrays need other exceptions
    'char[]': str,
    'void*': int,
    'void *': int
}


def get_git(url, splitString):
    rawContents = urllib.request.urlopen(url).read()
    decodedContents = rawContents.decode("utf-8")
    contents = decodedContents.split(splitString)
    return contents


def parse_frames(input):
    matches = CLASS_REGEX.findall(input)
    results = []
    for idx, match in enumerate(matches):
        lines = match[1].split('\n')
        items = []
        for line in lines:
            line = line.strip()

            # Skip empty or commented lines
            if not line or line.startswith('//'):
                continue

            # Remove trailing ;
            if line.endswith(';'):
                line = line[:-1]
            items.append(line.strip())

        results.append((match[0].strip(), items))
    return results

    # for result in results:
    #   print(result)


def parse_frame_enum(input):
    match = ENUM_REGEX.findall(input)[0]
    # print(matches)

    lines = match.split('\n')
    items = []
    for line in lines:
        line = line.strip()

        # Skip empty or commented lines
        if not line or line.startswith('//'):
            continue

        # Remove trailing ;
        if line.endswith(';'):
            line = line[:-1]
        items.append(line.strip())
    #    print(results)
    return items

    # for result in results:
    #   print(result)


def generate_frame_class(frames):
    # Write the file start
    output = "# this class was generated by Nicky's script on " + str(datetime.datetime.now()) + "\n\n"
    output += "from .common import Frame" + "\n"
    output += "from common.frame_enum import FrameType" + "\n"
    output += "import struct" + "\n\n\n"

    # For each frame int the file
    for frame in frames:

        # Get the elements of the class name
        classNameWords = frame[0][:-2].split("_")

        # The FrameType enumeration name
        frameType = '_'.join(classNameWords[1:]).upper()

        # Capitalize all the word in the class name to conform
        # to PEP-8
        for wordNr, word in enumerate(classNameWords):
            classNameWords[wordNr] = word.capitalize()

        # The frame format for in the class, follows
        # the format of the 'struct' Python 3.7 package
        frameFormat = ''

        # The length of the struct in bytes
        length = 0

        # A list of arguments for the 'set_data' method
        nameList = []
        typedList = []
        for type in frame[1]:
            split = type.split(' ')
            length += TYPE_SIZES[split[0]]
            frameFormat += TYPE_FORMATS[split[0]]
            nameList.append(split[1])
            typedList.append('{}: {}'.format(
                split[1], CORRESPONDING_TYPES[split[0]].__name__
            ))

        output += "class " + ''.join(classNameWords) + "(Frame):\n"
        output += "\tMEMBERS = [" + ', '.join(["'" + m + "'" for m in nameList]) + "]\n\n"
        output += "\tdef __init__(self):\n"
        output += "\t\tsuper(" + ''.join(classNameWords) + ", self).__init__()\n"
        output += "\t\tself.type = FrameType." + frameType + '\n'
        output += "\t\tself.format = '" + frameFormat + "'\n"
        output += "\t\tself.length = " + str(length) + "\n\n"
        output += "\tdef set_data(self, " + ', '.join(typedList) + '):\n'
        output += "\t\tself.data = struct.pack(self.format, " + ', '.join(nameList) + ')\n'
        output += "\n\n"
    return output


def generate_frame_enum(frames):
    # Write the file start
    output: str = "# this enum was generated by Nicky's and Lex's script on " + str(datetime.datetime.now()) + "\n\n"
    output += "from common.common import AutoNumber" + "\n\n\n"
    output += "class FrameType(AutoNumber):" + "\n"

    # For each frame in the file
    for frame in frames:
        # Take each frame, split by space and take first element, then remove trailing comma
        output += "\t" + frame.split(" ")[0].replace(",", "")
        output += frame[0][:-3] + " = ()\n"
    return output


def write_file(loc, filename, ext, content):
    # Write the output to the file
    with open((BASE_PATH / loc / (filename + ext)).resolve(), "w") as file:
        file.write(content.replace('\t', '    '))


write_file("common", "frames", ".py", generate_frame_class(parse_frames(get_git(SOURCE_URL, SOURCE_ANCHOR)[1])))
write_file("common", "frame_enum", ".py", generate_frame_enum(parse_frame_enum(get_git(SOURCE_URL, SOURCE_ANCHOR)[0])))