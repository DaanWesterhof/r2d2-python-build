"""
this file defines some configuration files
then defines some large parsing functions.

and finally uses those functions to generate frame_enum.py and frames.py
"""

import re
import urllib.request
import datetime
from pathlib import Path
from collections import namedtuple

REGEX_FLAGS = re.IGNORECASE | re.MULTILINE | re.DOTALL
FRAME_REGEX = re.compile(
    r'(?:\/\*{2}((?:(?!\*\/).)*?)\*\/\s+struct )?(frame\w+) \{(.*?)\}', REGEX_FLAGS)
CLI_FLAG_REGEX = re.compile(
    r'@cond CLI COMMAND @endcond.*?\n(.*)', REGEX_FLAGS)
COMMENT_REGEX = re.compile(r'\*(.*?)\n')
ENUM_REGEX = re.compile(
    r'frame_id ?\{(.+?)\}', REGEX_FLAGS)

RAW_GITHUB = "https://raw.githubusercontent.com/"
REPOSITORY = "R2D2-2019/internal_communication/"
BRANCH = "master"
SOURCE_FILE = "/code/headers/frame_types.hpp"
SOURCE_URL = RAW_GITHUB + REPOSITORY + BRANCH + SOURCE_FILE

SOURCE_ANCHOR = "/** #PythonAnchor# */"
BASE_PATH = Path(__file__).parent.parent

CppType = namedtuple("CPP_TYPE", ['format', 'size', 'python_type'])

TYPE_TABLE = {
    'char':                 CppType(format='c', size=1, python_type=str),
    'int8_t':               CppType(format='c', size=1, python_type=int),
    'signed char':          CppType(format='b', size=1, python_type=str),
    'unsigned char':        CppType(format='B', size=1, python_type=str),
    'uint8_t':              CppType(format='B', size=1, python_type=int),
    '_Bool':                CppType(format='?', size=1, python_type=bool),
    'bool':                 CppType(format='?', size=1, python_type=bool),
    'short':                CppType(format='h', size=2, python_type=int),
    'int16_t':              CppType(format='h', size=2, python_type=int),
    'unsigned short':       CppType(format='H', size=2, python_type=int),
    'uint16_t':             CppType(format='H', size=2, python_type=int),
    'int':                  CppType(format='i', size=4, python_type=int),
    'int32_t':              CppType(format='i', size=4, python_type=int),
    'unsigned int':         CppType(format='I', size=4, python_type=int),
    'uint32_t':             CppType(format='I', size=4, python_type=int),
    # GCC 8.2 ARM has sizeof(long) == 4, sizeof(long long) == 8
    'long':                 CppType(format='l', size=4, python_type=int),
    'int64_t':              CppType(format='l', size=4, python_type=int),
    'unsigned long':        CppType(format='L', size=4, python_type=int),
    'uint64_t':             CppType(format='L', size=8, python_type=int),
    'long long':            CppType(format='q', size=8, python_type=int),
    'unsigned long long':   CppType(format='Q', size=8, python_type=int),
    'ssize_t':              CppType(format='n', size=4, python_type=int),
    'size_t':               CppType(format='N', size=4, python_type=int),
    'float':                CppType(format='f', size=4, python_type=float),
    'double':               CppType(format='d', size=8, python_type=float),
    'char[]':               CppType(format='s', size=4, python_type=str),
    'void*':                CppType(format='P', size=4, python_type=int),
    'void *':               CppType(format='P', size=4, python_type=int),
}

def parse_cpp(input_string, regex=FRAME_REGEX):
    classes = []
    for match in regex.findall(input_string):
        cpp_class = Class(match[1].strip(), [], [])
        # parse description
        cli_description = CLI_FLAG_REGEX.findall(match[0])
        if cli_description:
            cpp_class.doc_string.extend([
                line.strip() for line in COMMENT_REGEX.findall(cli_description[0])
            ])
        # parse function body
        for line in match[2].split('\n'):
            line = line.strip()
            if line.endswith((';', ',')):
                line = line[:-1]
            if not line or line.startswith('//'):
                continue
            cpp_class.members.append(line)
        classes.append(cpp_class)
    return classes




def parse_frames(input_string: str):
    matches = FRAME_REGEX.findall(input_string)

    results = []
    for idx, match in enumerate(matches):
        cli_description = CLI_FLAG_REGEX.findall(match[0])
        if cli_description:
            cli_description = [
                line.strip() for line in COMMENT_REGEX.findall(cli_description[0])
            ]

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
        class_name_words = frame[0][:-2].split("_")

        # The FrameType enumeration name
        frame_type = '_'.join(class_name_words[1:]).upper()

        # Capitalize all the word in the class name to conform
        # to PEP-8
        class_name_words = list(map(str.capitalize, class_name_words))

        # The frame format for in the class, follows
        # the format of the 'struct' Python 3.7 package
        frame_format = ''

        # The length of the struct in bytes
        length = 0

        # A list of arguments for the 'set_data' method
        name_list = []
        typed_list = []
        for data_member in frame.members:
            member_type, member_name = data_member.split(' ')
            cpp_type = TYPE_TABLE[member_type]
            length += cpp_type.size
            frame_format += cpp_type.format
            name_list.append(member_name)
            typed_list.append('{}: {}'.format(
                member_name, cpp_type.python_type.__name__
            ))

        output += "class " + ''.join(class_name_words) + "(Frame):\n"
        output += "\tMEMBERS = [" + \
            ', '.join(["'" + m + "'" for m in name_list]) + "]\n"
        output += "\tDESCRIPTION = \""
        for line in frame[2]:
            output += line + '\\n'
        output += "\"\n\n"
        output += "\tdef __init__(self):\n"
        output += "\t\tsuper(" + ''.join(class_name_words) + \
            ", self).__init__()\n"
        output += "\t\tself.type = FrameType." + frame_type + '\n'
        output += "\t\tself.format = '" + frame_format + "'\n"
        output += "\t\tself.length = " + str(length) + '\n\n'
        output += "\tdef set_data(self, " + ', '.join(typed_list) + '):\n'
        output += "\t\tself.data = struct.pack(self.format, " + \
            ', '.join(name_list) + ')\n'
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

def get_git(url: str, split_string: str) -> list:
    """returns the file specified in the url as text, split with split_string"""
    return (
        urllib.request.urlopen(url)
        .read()
        .decode("utf-8")
        .split(split_string)
    )

def write_file(loc, filename, ext, content):
    # Write the output to the file
    with open((BASE_PATH / loc / (filename + ext)).resolve(), "w") as file:
        file.write(content.replace('\t', '    '))

def _path(loc, filename):
    return (BASE_PATH / loc / filename).resolve()

if __name__ == "__main__":
    write_file(
        "common", "frames", ".py",
        content=generate_frame_class(parse_frames(get_git(SOURCE_URL, SOURCE_ANCHOR)[1])))
    write_file(
        "common", "frame_enum", ".py",
        content=generate_frame_enum(parse_frame_enum(get_git(SOURCE_URL, SOURCE_ANCHOR)[0])))
