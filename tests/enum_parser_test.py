#! python

"""tests tooling/enum_parser"""

import types
from tooling import enum_parser

TEST_SET = ["enum class test_item_" + str(i) + " : uint8_t {A, B, C};" for i in range(10)]

def test_get_enum_strings():
    """Tests if the get_enum_strings in enum_parser.py is working properly """
    enum_string = ""
    # Copies the components item to a local variable
    components = TEST_SET
    # Wraps all items into a single string
    for component in components:
        enum_string += component
    enum_strings = enum_parser.get_enum_strings(enum_string)
    # Checks if the enum strings type is a generator  (For performance purposes
    assert isinstance(enum_strings, types.GeneratorType)
    # Convert the generator to a list, so the output can be tested multiple times
    item_list = [item for item in enum_strings]
    # Checks if the amount of recognized strings is correct
    assert len(item_list) == 10
    # Checks if all outputs are strings
    for item in item_list:
        assert isinstance(item, str)
    # Checks if all outputs are the same as the seperated inputs
    for index, item in enumerate(item_list):
        assert components[index] == item


def test_get_enum_definition():
    """Tests if the get_get_enum_definition in enum_parser.py is working properly """
    enum_string = "enum class test_item: uint8_t {A, B, C, D};"
    # The test dataset, a enum class, with name test_item, type uint8_t and 4 items, A trough D
    enum_object: enum_parser.CxxEnum = enum_parser.get_enum_definition(enum_string)
    # Checks if the name is correct
    assert enum_object.name == "test_item"
    # Checks if the type is correct
    assert enum_object.inner_type == "uint8_t"
    # Checks if the items are correc
    assert enum_object.items == {'A': None, 'B': None, 'C': None, 'D':None}

if __name__ == "__main__":
    test_get_enum_strings()
    test_get_enum_definition()
