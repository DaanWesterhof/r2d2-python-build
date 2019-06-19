#! python

"""this module defines functions for parsing c++ enums"""

import urllib.request
import re
import datetime

__author__ = "Sebastiaan Saarloos"
__date__ = datetime.date(2019, 6, 3)
__status__ = "Developing"
__maintainer__ = "Isha Geurtsen"

class CxxEnum:
    """Class that defines an Enumeration in C++"""
    def __init__(self, name: str, inner_type: str, items: list):
        """Initializes the enum class"""
        self.name: str = name
        self.inner_type: str = inner_type
        self.items: 'list[str]' = items

    def __len__(self) -> int:
        """Gives the number of items inside the enum"""
        return len(self.items)

    def __repr__(self) -> str:
        """Gives a representation in a string inside"""
        return f"{self.name} : {self.inner_type} {self.items.__repr__()}"

    def __iter__(self) -> str:
        """Iterates over all the items inside the enum"""
        for item in self.items:
            yield item




def get_enum_strings(file_contents: str) -> list:
    """Scrapes all the enum strings from a given string"""
    # Remove all comments from the file.
    file_contents = re.sub(r"//.*\n", "", file_contents)
    # Remove redundant spaces
    file_contents = re.sub(r"\s+", " ", file_contents)
    # enum class regular expression
    pattern = re.compile("enum class\\s*\\w+\\s*\\:\\s*\\w+\\s*\\{[^\\{\\}]+\\};")
    # Iterates over all the matches, and will yield returned
    for item in pattern.finditer(file_contents):
        # Yield, means: give back a single item, go further a new item is requested
        yield item.group(0).replace("\n", "")


def get_enum_definition(enum_string: str) -> CxxEnum:
    """Converts a enum definition represented as a string to a CXX enum object"""
    # Get the name of the enum
    name = re.findall(r"(?<=enum class )\w+", enum_string)[0]
    # Get the defined type of the enum
    inner_type = re.findall(r":\s*(\w+)", enum_string)[0]
    # Get all the items of that are defined inside the enum class
    inner_items = re.findall(r"\{([^{}]+)\}", enum_string)[0].replace(" ", "").split(",")
    return CxxEnum(name, inner_type, inner_items)

def get_github_file(repository: str, branch: str, file: str):
    """Helper function to get a github file from a given repository"""
    url = (
        "https://raw.githubusercontent.com/R2D2-2019/" +
        f"{repository}/{branch}/{file}")
    return (
        urllib.request.urlopen(url)
        .read()
        .decode("utf-8")
    )
def get_enum_definitions() -> list:
    """collect enums defined in the frame_enums.hpp from the external communications file"""
    # Get the file from GitHub
    file_content = get_github_file(
        "internal_communication",
        "master",
        "code/headers/frame_enums.hpp"
    )
    # Seperate file in seperate enum strings
    enum_strings = get_enum_strings(file_content)
    # Loop over all enum strings
    for enum_string in enum_strings:
        yield get_enum_definition(enum_string)



if __name__ == "__main__":
    for definition in get_enum_definitions():
        print(definition)
