import sys
import urllib.request
import re

class CxxEnum:
    def __init__(self, name: str, inner_type: str, items: list):
        self.name: str = name
        self.inner_type: str = inner_type
        self.items: list[str] = items

    def __repr__(self):
        return f"{self.name} : {self.inner_type} {self.items.__repr__()}"




def get_enum_strings(file_contents: str) -> list:
    # Remove comments
    file_contents = re.sub("//.*\n", "", file_contents)
    #remove redundant spaces
    file_contents = re.sub("\s+", " ", file_contents)
    pattern = re.compile("enum class\\s*\\w+\\s*\\:\\s*\\w+\\s*\\{[^\\{\\}]+\\}")
    return [item.replace("\n", "") for item in pattern.findall(file_contents)]


def get_enum_definition(enum_string: str):
    name = re.findall("(?<=enum class )\w+", enum_string)[0]
    inner_type = re.findall(":\s\w+", enum_string)[0][3:]
    inner_items = re.findall("\{[^{}]+\}", enum_string)[0][1:-2].replace(" ", "").split(",")
    return CxxEnum(name, inner_type, inner_items)



if __name__ == "__main__":
    file_content = (
        urllib.request.urlopen(
            "https://raw.githubusercontent.com/R2D2-2019/internal_communication/master/code/headers/frame_enums.hpp")
            .read()
            .decode("utf-8")
    )
    enum_strings = get_enum_strings(file_content)
    for enum_string in enum_strings:
        print(get_enum_definition(enum_string))

