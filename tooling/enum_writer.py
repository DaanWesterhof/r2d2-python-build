#! python

from tooling.enum_parser import CxxEnum
import datetime

def get_enum_file_header(maintainer: str, date: datetime.datetime, status: str = "Production"):
    return f"""
    #! python

    \""" this generated file defines Frames

    it is based on the definitons of https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_types.hpp

    if you have a question or a problem.
    please make a github issue on https://github.com/R2D2-2019/r2d2-python-build/issues/new
    or look at https://github.com/R2D2-2019/r2d2-python-build#faq
    \"""

    from common.common import AutoNumber

    __maintainer__ = "{maintainer}"
    __date__ = "{date}"
    __status__ = "{status}"
    """





def convert_enum_to_python(cxx_enum_object: CxxEnum) -> str:
    """Create a string representation of thje CxxEnum object in Python"""
    # Create class signature 
    text = F"class {cxx_enum_object.name}(AutoNumber): \n"
    # Add all items to the classs definition
    for item in cxx_enum_object:
        text += f"    {item} = ()\n"
    # Return the string
    return text

def convert_enums_to_fileformat(enum_text_list: list):
    """Create the fileformat for the enum file"""
    # Generate a file header
    file = get_enum_file_header("Sebastiaan Saarloos", datetime.datetime.now(), "Production") + '\n'
    # Iterate over all enum strings
    for enum_text in enum_text_list:
        file += enum_text + '\n'
    # Give back the file contents
    return file








if __name__ == "__main__":
    convert_enum_to_python(CxxEnum("HelloWorld", "uint8_t", ["Hello", "World"]))
