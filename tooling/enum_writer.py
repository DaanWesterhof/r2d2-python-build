#! python

"""functions for generating a python file from c++ enums
in the form of cxx enums"""

import datetime
from tooling.enum import Enum

_ENUM_FILE_HEADER = """
#! python

\""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
\"""

import enum

__maintainer__ = "{maintainer}"
__date__ = "{date}"
__status__ = "{status}"
"""




def write_enums_to_file(file, enums: 'list[tooling.Enum]'):
    """Create the fileformat for the enum file"""
    # write the file header to file
    file.write(_ENUM_FILE_HEADER.format(
        maintainer="Sebastiaan Saarloos",
        date=datetime.datetime.now(),
        status="Production"
    ))
    # write the enums to file
    for enum in enums:
        enum: Enum
        file.write(str(enum))
