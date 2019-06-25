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
from functools import reduce
from tooling import enum_parser, enum_writer
from tooling.enum_converter import PythonEnum

REGEX_FLAGS = re.IGNORECASE | re.MULTILINE | re.DOTALL
FRAME_REGEX = re.compile(
    r'(?:\/\*{2}((?:(?!\*\/).)*?)\*\/\s+struct )?(frame\w+)[\s\w\:]*\{(.*?)\}', REGEX_FLAGS)
CLI_FLAG_REGEX = re.compile(
    r'@cond CLI COMMAND @endcond.*?\n(.*)', REGEX_FLAGS)
COMMENT_REGEX = re.compile(r'\*(.*?)\n')

RAW_GITHUB = "https://raw.githubusercontent.com/"
REPOSITORY = "R2D2-2019/internal_communication/"
BRANCH = "master"
SOURCE_FILE = "/code/headers/frame_types.hpp"
SOURCE_URL = RAW_GITHUB + REPOSITORY + BRANCH + SOURCE_FILE

CppType = namedtuple("CppType", ['format', 'size', 'python_type'])
Class = namedtuple("Frame", ["name", "members", "doc_string"])


TYPE_TABLE = {
    'char':                 CppType(format='c', size=1, python_type=str),
    'int8_t':               CppType(format='b', size=1, python_type=int),
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
def parse_cpp(input_string: str, regex: re.Pattern = FRAME_REGEX) -> ...:
    """
    this method parses the input_string using the regex pattern
    and compiles a list of Class objects containing every c++ class

    :input_string: a string containing c++ code.
    :regex: a regex pattern, to be used to parse c++ structs and classes
    :return: a list() containg Class() objects
    """
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


HEADER = """#! python

\""" this generated file defines Frames

it is based on the definitons of {url}

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
\"""

{imports}

__maintainer__ = "Isha Geurtsen"
__date__ = "{date}"
__status__ = "Production"
"""

FRAME_TEMPLATE = """class {frame_name}(Frame):
    MEMBERS = [{attribute_names}]
    DESCRIPTION = "{description}"

    def __init__(self):
        super({frame_name}, self).__init__()
        self.type = FrameType.{frame_type}
        self.format = '{frame_format}'
        self.length = {size}

    def set_data(self, {attributes_typed}):
        self.data = struct.pack(self.format, {attributes})


"""


def generate_frame_class(frames):
    """generates the body of a python file that defines the c++ frames"""
    # Write the file start
    output = HEADER.format(
        date=datetime.datetime.now(),
        url=SOURCE_URL,
        imports="\n".join([
            "import struct",
            "from .common import Frame",
            "from common.frame_enum import FrameType"
        ]),
    )

    # For each frame int the file
    for frame in frames:

        frame_name = "".join(map(str.capitalize, frame.name.split("_")[:-1]))

        # The FrameType enumeration name
        frame_type = '_'.join(frame.name.split("_")[1:-1]).upper()

        # The frame format for in the class, follows
        # the format of the 'struct' Python 3.7 package
        frame_format = []

        # The size of the struct in bytes
        size = 0

        # A list of arguments for the 'set_data' method
        name_list = []
        typed_list = []
        for data_member in frame.members:
            match = re.match(r"(char) (\w+)\[(\d*)\]", data_member)
            if match:
                member_type, member_name, member_size = match.groups()
                if not member_size:
                    member_size = "255"
                member_type = CppType(str(int(member_size))+"s", int(member_size), str)
            else:
                member_type, member_name = data_member.split(' ')
                member_type = TYPE_TABLE[member_type]
            size += member_type.size
            frame_format.append(member_type.format)
            name_list.append(member_name)
            typed_list.append('{}: {}'.format(
                member_name, member_type.python_type.__name__))
        output += FRAME_TEMPLATE.format(
            frame_name=frame_name,
            attribute_names=', '.join(["'" + m + "'" for m in name_list]),
            description='\\n'.join(frame.doc_string),
            frame_type=frame_type,
            frame_format=" ".join(frame_format),
            size=size,
            attributes_typed=', '.join(typed_list),
            attributes=', '.join(name_list),
        )
    return output


def generate_frame_enum(frames):
    """generates the body of a python file that defines the c++ frame type enum"""

    # Write the file start
    output = HEADER.format(
        date=datetime.datetime.now(),
        url=SOURCE_URL,
        imports="from common.common import AutoNumber"
    )

    output += "class FrameType(AutoNumber):\n"

    frame_type = reduce((lambda a, b: b if b.name == "frame_type" else a), frames, None)
    assert frame_type is not None
    # For each frame in the file
    for frame in frame_type.members:
        # Take each frame, split by space and take first element
        output += " "*4 + frame.split(" ")[0]
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


SOURCE_ANCHOR = "/** #PythonAnchor# */"

BASE_PATH = Path(__file__).parent.parent


def _path(loc, filename):
    return (BASE_PATH / loc / filename).resolve()


if __name__ == "__main__":
    ENUM_TEXT, FRAME_TEXT = get_git(SOURCE_URL, SOURCE_ANCHOR)
    ENUMS = list(enum_parser.get_enum_definitions())
    enum: enum_parser.CxxEnum
    for enum in ENUMS:
        if enum.inner_type not in TYPE_TABLE.keys():
            continue
        TYPE_TABLE[enum.name] = TYPE_TABLE[enum.inner_type]


    with open(_path('common', 'frames.py'), 'w') as frames_file:
        frames_file.write(generate_frame_class(parse_cpp(FRAME_TEXT)))
    with open(_path('common', 'frame_enum.py'), 'w') as frame_enum_file:
        frame_enum_file.write(generate_frame_enum(parse_cpp(ENUM_TEXT)))

    with open(_path('common', 'enums.py'), 'w') as enum_file:
        enum_writer.write_enums_to_file(
            file=enum_file,
            enums=(PythonEnum.from_enum(enum) for enum in ENUMS),
        )
