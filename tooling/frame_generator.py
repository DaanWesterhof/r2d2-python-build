"""
this file defines some configuration files
then defines some large parsing functions.

and finally uses those functions to generate frame_enum.py and frames.py
"""

import re
import urllib.request
import datetime
from pathlib import Path


FRAME_REGEX = re.compile(r'(?:\/\*{2}((?:(?!\*\/).)*?)\*\/\s+struct )?(frame\w+) \{(.*?)\}', re.IGNORECASE | re.MULTILINE | re.DOTALL)
CLI_FLAG_REGEX = re.compile(r'@cond CLI COMMAND @endcond.*?\n(.*)', re.IGNORECASE | re.MULTILINE | re.DOTALL)
COMMENT_REGEX = re.compile(r'\*(.*?)\n')
ENUM_REGEX = re.compile(r'frame_id ?\{(.+?)\}', re.IGNORECASE | re.MULTILINE | re.DOTALL)

RAW_GITHUB = "https://raw.githubusercontent.com/"
REPOSITORY = "R2D2-2019/internal_communication/"
BRANCH = "master"
SOURCE_FILE = "/code/headers/frame_types.hpp"
SOURCE_URL = RAW_GITHUB + REPOSITORY + BRANCH + SOURCE_FILE

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


def get_git(url, split_string: str):
    rawContents = urllib.request.urlopen(url).read()
    decodedContents = rawContents.decode("utf-8")
    contents = decodedContents.split(split_string)
    return contents


def parse_frames(input_string: str):
    matches = FRAME_REGEX.findall(input_string)

    results = []
    for idx, match in enumerate(matches):
        cli_description = CLI_FLAG_REGEX.findall(match[0])
        if cli_description:
            cli_description = [line.strip() for line in COMMENT_REGEX.findall(cli_description[0])]

        lines = match[2].split('\n')
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

        results.append((match[1].strip(), items, cli_description))
    return results


def parse_frame_enum(input_string: str):
    match = ENUM_REGEX.findall(input_string)[0]

    lines = match.split('\n')
    items = []
    for line in lines:
        line = line.strip()

        # Skip empty or commented lines
        if not line or line.startswith('//'):
            continue

        # Remove trailing ,
        if line.endswith(','):
            line = line[:-1]
        items.append(line.strip())
    return items


def generate_frame_class(frames):
    # Write the file start
    output = (
        "# this class was generated by Nicky's script on "
        + str(datetime.datetime.now()) + "\n\n"
        + "from .common import Frame" + "\n"
        + "from common.frame_enum import FrameType" + "\n"
        + "import struct" + "\n\n\n"
    )

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
        output += "\tMEMBERS = [" + ', '.join(["'" + m + "'" for m in nameList]) + "]\n"
        output += "\tDESCRIPTION = \""
        for line in frame[2]:
            output += line + '\\n'
        output += "\"\n\n"
        output += "\tdef __init__(self):\n"
        output += "\t\tsuper(" + ''.join(classNameWords) + ", self).__init__()\n"
        output += "\t\tself.type = FrameType." + frameType + '\n'
        output += "\t\tself.format = '" + frameFormat + "'\n"
        output += "\t\tself.length = " + str(length) + '\n\n'
        output += "\tdef set_data(self, " + ', '.join(typedList) + '):\n'
        output += "\t\tself.data = struct.pack(self.format, " + ', '.join(nameList) + ')\n'
        output += "\n\n"
    return output


def generate_frame_enum(frames):
    # Write the file start
    output: str = (
        "# this enum was generated by Nicky's and Lex's script on "
        + str(datetime.datetime.now()) + "\n\n"
        + "from common.common import AutoNumber" + "\n\n\n"
        + "class FrameType(AutoNumber):" + "\n"
    )

    # For each frame in the file
    for frame in frames:
        # Take each frame, split by space and take first element
        output += "\t" + frame.split(" ")[0]
        output += frame[0][:-3] + " = ()\n"
    return output


def write_file(loc, filename, ext, content):
    # Write the output to the file
    with open((BASE_PATH / loc / (filename + ext)).resolve(), "w") as file:
        file.write(content.replace('\t', '    '))

if __name__ == "__main__":
    write_file(
        "common", "frames", ".py",
        content=generate_frame_class(parse_frames(get_git(SOURCE_URL, SOURCE_ANCHOR)[1])))
    write_file(
        "common", "frame_enum", ".py",
        content=generate_frame_enum(parse_frame_enum(get_git(SOURCE_URL, SOURCE_ANCHOR)[0])))
