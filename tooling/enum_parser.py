import sys
import urllib.request
import re

class CxxEnum:
    """Class that defines an Enumeration in C++"""
    def __init__(self, name: str, inner_type: str, items: list):
        """Initializes the enum class"""
        self.name: str = name
        self.inner_type: str = inner_type
        self.items: list[str] = items

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
    # Remove comments
    print(file_contents)
    file_contents = re.sub("//.*\n", "", file_contents)
    #remove redundant spaces
    file_contents = re.sub("\s+", " ", file_contents)
    pattern = re.compile("enum class\\s*\\w+\\s*\\:\\s*\\w+\\s*\\{[^\\{\\}]+\\};")
    # return [item.replace("\n", "") for item in pattern.findall(file_contents)]
    for item in pattern.findall(file_contents):
        yield item.replace("\n", "")


def get_enum_definition(enum_string: str):
    name = re.findall("(?<=enum class )\w+", enum_string)[0]
    inner_type = re.findall(":\s*(\w+)", enum_string)[0]
    inner_items = re.findall("\{([^{}]+)\}", enum_string)[0].replace(" ", "").split(",")
    return CxxEnum(name, inner_type, inner_items)

def get_github_file(repository: str, branch: str, file: str):
    return (
        urllib.request.urlopen(
            f"https://raw.githubusercontent.com/R2D2-2019/{repository}/{branch}/{file}")
            .read()
            .decode("utf-8")
    )
def get_enum_definitions():
    file_content = get_github_file("internal_communication", "master", "code/headers/frame_enums.hpp")
    enum_strings = get_enum_strings(file_content)
    for enum_string in enum_strings:
        yield get_enum_definition(enum_string)



def convert_to_python(enum: CxxEnum):
    enum


if __name__ == "__main__":
    definitions = get_enum_definitions()
    for definition in definitions:
        print(definition)

