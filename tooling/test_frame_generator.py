"tests tooling/frame_generator"

import tooling.frame_generator

# ! does not test get_gid

def remove_leading_line(string: str)->str:
    return string.split(sep='__status__ = "Production"', maxsplit=1)[1]

def test_type_table():
    "tests that the TYPE_TABLE from frame_generator is created properly"
    type_table = tooling.frame_generator.TYPE_TABLE
    assert isinstance(type_table, dict)
    for key, value in type_table.items():
        assert isinstance(key, str)

        assert isinstance(value.format, str)
        assert len(value.format) == 1

        assert isinstance(value.size, int)
        assert value.size >= 0

        assert isinstance(value.python_type, type)
        assert value.python_type in (str, int, bool, float)

def test_parse_frames():
    """tests that frames classsare generated properly"""
    parse_cpp = tooling.frame_generator.parse_cpp
    Class = tooling.frame_generator.Class
    input_string = """
    class frame_test_frame {
        bool flag;
    }
    """.strip()
    expected_output = [Class("frame_test_frame", ['bool flag'], [])]

    output = parse_cpp(input_string)
    assert output == expected_output

def test_parse_frame_enum():
    # frame_id.?\{(.+?)\}
    parse_frame_enum = tooling.frame_generator.parse_cpp
    input_string = """
    enum frame_test : frame_id {
        NONE = 0,
        TEST,
        ALL,
        COUNT
    }
    """.strip()
    expected_output = ['NONE = 0', 'TEST', 'ALL', 'COUNT']
    output = parse_frame_enum(input_string)[0].members
    assert output == expected_output

def test_generate_frame_class():
    generate_frame_class = tooling.frame_generator.generate_frame_class
    Class = tooling.frame_generator.Class
    input_frames = [Class("frame_test_frame_s", ['bool flag'], [])]
    expected_output = """
class FrameTestFrame(Frame):
    MEMBERS = ['flag']
    DESCRIPTION = ""

    def __init__(self):
        super(FrameTestFrame, self).__init__()
        self.type = FrameType.TEST_FRAME
        self.format = '?'
        self.length = 1

    def set_data(self, flag: bool):
        self.data = struct.pack(self.format, flag)


"""
    output = generate_frame_class(input_frames)
    assert remove_leading_line(output) == expected_output

def test_generate_frame_enums():
    generate_frame_enum = tooling.frame_generator.generate_frame_enum
    Class = tooling.frame_generator.Class
    input_frames = [Class('frame_id', ['NONE = 0', 'TEST', 'ALL', 'COUNT'], [])]
    expected_output = """
class FrameType(AutoNumber):
    NONE = ()
    TEST = ()
    ALL = ()
    COUNT = ()
"""
    output = generate_frame_enum(input_frames)
    assert remove_leading_line(output) == expected_output

def test_CLI_flag():
    parse_frames = tooling.frame_generator.parse_cpp
    input_string = r"""
    /** @cond CLI COMMAND @endcondtest
     * Packet containing the state of
     * a button.
     */
    struct frame_button_state_s {
        bool pressed;
    };
    """
    expected_output = [
        ('frame_button_state_s', ['bool pressed'], ['Packet containing the state of', 'a button.'])]
    output = parse_frames(input_string)
    assert expected_output == output

def test_CLI_flag_parse_frames_negative():
    """this test makes sure only the correct c++ doc string gets parsed."""
    parse_frames = tooling.frame_generator.parse_cpp
    input_string = r"""
    /** @cond CLI COMMAND @endcond
     * BAD comment
     */

    /** @cond CLI COMMAND @endcond
     * GOOD comment
    */
    struct frame_button_state_s {
        bool pressed;
    };
    """
    expected_output = [('frame_button_state_s', ['bool pressed'], ['GOOD comment'])]
    output = parse_frames(input_string)
    assert expected_output == output

def test_CLI_flag_generate_frame_class():
    generate_frame_class = tooling.frame_generator.generate_frame_class
    Class = tooling.frame_generator.Class
    input_frames = [Class(
        "frame_button_state_s",
        ['bool pressed'],
        ['Packet containing the state of', 'a button.'])]
    expected_output = """
class FrameButtonState(Frame):
    MEMBERS = ['pressed']
    DESCRIPTION = "Packet containing the state of\\na button."

    def __init__(self):
        super(FrameButtonState, self).__init__()
        self.type = FrameType.BUTTON_STATE
        self.format = '?'
        self.length = 1

    def set_data(self, pressed: bool):
        self.data = struct.pack(self.format, pressed)


"""
    output = generate_frame_class(input_frames)
    assert remove_leading_line(output) == expected_output
