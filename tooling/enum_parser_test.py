import tooling.enum_parser as enum_parser
import types


TEST_SET = components = ["enum class test_item_" + str(i) + " : uint8_t {A, B, C};" for i in range(10)]

def test_get_enum_strings():
    enum_string = ""
    components = TEST_SET
    for component in components:
        enum_string += component
    enum_strings = enum_parser.get_enum_strings(enum_string)
    assert isinstance(enum_strings, types.GeneratorType)
    item_list = [item for item in enum_strings]
    assert len(item_list) == 10
    for item in item_list:
        assert isinstance(item, str)
    for i in range(len(item_list)):
        assert components[i] == item_list[i]


def test_get_enum_definition():
    enum_string = "enum class test_item: uint8_t {A, B, C, D};"
    enum_object: enum_parser.CxxEnum = enum_parser.get_enum_definition(enum_string)
    print(enum_object)
    assert enum_object.name == "test_item"
    assert enum_object.inner_type == "uint8_t"
    assert enum_object.items == ['A', 'B', 'C', 'D']


if __name__ == "__main__":
    test_get_enum_strings()
    test_get_enum_definition()