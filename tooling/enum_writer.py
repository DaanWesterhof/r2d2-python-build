from tooling.enum_parser import CxxEnum
HEADER = """
#! python
\""" this generated file defines Frames

it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

if you have a question or a problem.
please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
or look at https://github.com/R2D2-2019/r2d2-python-build#faq
\"""

from common.common import AutoNumber

__maintainer__ = "Sebastiaan Saarloos"
__date__ = "2019-06-04 17:09:01.153106"
__status__ = "Production"
"""


def convert_enum_to_python(cxx_enum_object: CxxEnum) -> str:
    text = F"class {cxx_enum_object.name}(AutoNumber): \n"
    for item in cxx_enum_object:
        text += f"    {item} = ()\n"
    return text

def convert_enums_to_fileformat(enum_text_list: list):
    file = HEADER + '\n'
    for enum_text in enum_text_list:
        file += enum_text + '\n'
    return file








if __name__ == "__main__":
    convert_enum_to_python(CxxEnum("HelloWorld", "uint8_t", ["Hello", "World"]))
