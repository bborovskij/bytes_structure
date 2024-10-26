import struct

import pytest
from byte_structure.bytes_structure import Field, ByteStructureBase, Errors

data = bytearray(
    [
        0x01,
        0x04,
        0x08,
        0x0B,
        0xF,
        0x10,
        0x40,
        0x01,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0x0F,
        0xFF,
    ]
)


@pytest.fixture
def command_cls():
    class Command(ByteStructureBase):
        one_byte = Field(">B")
        two_bytes = Field(">H")

    return Command


@pytest.fixture
def command_cls_v2(command_cls):
    class CommandV2(command_cls):
        four_bytes = Field(">I")

    return CommandV2


@pytest.fixture
def command_cls_v3(command_cls_v2):
    class CommandV3(command_cls_v2):
        sixteen_bytes = Field(">16s")

    return CommandV3


@pytest.fixture
def var_len_command_cls__and__data():
    class BaseMessage(ByteStructureBase):
        field_1 = Field(">H")

    class DerivedMessage(BaseMessage):
        len = Field(">B")
        var_len_field = Field(lambda self: f">{self.len}s")

    class DerivedMessageV2(DerivedMessage):
        len_v2 = Field(">B")
        var_len_field_v2 = Field(lambda self: f">{self.len_v2}s")

    return DerivedMessageV2, b"\x00\x01\x05hello\x05world"


def test_base_message_correct_values(command_cls):
    command = command_cls(data)

    expected = struct.unpack_from(">BH", data, 0)
    assert expected == (command.one_byte, command.two_bytes)


def test_base_message_correct_names(command_cls):
    command = command_cls(data)
    assert ("one_byte", "two_bytes") == tuple(command.parsed_fields_map.keys())


def test_base_message_correct_inheritance(command_cls, command_cls_v2, command_cls_v3):
    command = command_cls(data)
    command_v2 = command_cls_v2(data)
    command_v3 = command_cls_v3(data)

    assert command_v3.one_byte == command.one_byte == command_v2.one_byte
    assert command_v3.two_bytes == command.two_bytes == command_v2.two_bytes
    assert command_v3.four_bytes == command_v2.four_bytes
    assert (
        command_v3.sixteen_bytes
        == b"\x01\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\xff"
    )


def test_base_message_correct_repr(command_cls_v2):
    cmd_v2 = command_cls_v2(data)
    expected_rep = (
        "CommandV2:\r\n-- one_byte 1\r\n-- two_bytes 1032\r\n-- four_bytes 185536576"
    )
    assert expected_rep == str(cmd_v2)


def test_base_message_gather_fields(command_cls_v2):
    cmd_v2 = command_cls_v2(data)
    fields_map = cmd_v2.get_fields_and_their_names()
    assert ("one_byte", "two_bytes", "four_bytes") == tuple(fields_map.keys())
    assert all(map(lambda o: isinstance(o, Field), fields_map.values()))


def test_base_message_can_get_fmt_from_field(command_cls_v2):
    cmd_v2 = command_cls_v2(data)
    field_objs = cmd_v2.get_fields_and_their_names().values()
    fmts = [field.get_fmt(cmd_v2) for field in field_objs]
    assert len(fmts) == len(field_objs)


def test_base_message_correct_size(command_cls_v2):
    cmd_v2 = command_cls_v2(data)
    assert cmd_v2.get_expected_size() == 7


def test_base_var_len_field(var_len_command_cls__and__data):
    cls, data = var_len_command_cls__and__data
    parsed_msg = cls(data)
    assert parsed_msg.var_len_field == b"hello"
    assert parsed_msg.var_len_field_v2 == b"world"


def test_base_get_size_var_len(var_len_command_cls__and__data):
    cls, data = var_len_command_cls__and__data
    parsed_msg = cls(data)
    assert parsed_msg.get_expected_size() == len(data)


def test_base_repr_var_len(var_len_command_cls__and__data):
    cls, data = var_len_command_cls__and__data
    parsed_msg = cls(data)
    expected_repr = (
        "DerivedMessageV2:\r\n"
        "-- field_1 1\r\n"
        "-- len 5\r\n"
        "-- var_len_field b'hello'\r\n"
        "-- len_v2 5\r\n"
        "-- var_len_field_v2 b'world'"
    )
    assert expected_repr == str(parsed_msg)


def test_base_var_len_when_len_specified_in_v1():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg = b"\x00\x05hello"

    parsed = DerivedMessage(msg)
    assert parsed.len == 5
    assert parsed.var_len_field == b"hello"


def test_base_var_len_when_len_specified_before():
    class BaseMessage(ByteStructureBase):
        var_len_field = Field(lambda self: f">{self.len}s")

    class DerivedMessage(BaseMessage):
        len = Field(">H")

    msg = b"hello\x00\x05"

    with pytest.raises(Errors.LenNotFoundInMessageError):
        DerivedMessage(msg)


def test_base_var_len_when_no_len_specified():
    class BaseMessage(ByteStructureBase):
        two_bytes = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg = b"hello\x00\x05"

    with pytest.raises(Errors.LenNotFoundInMessageError):
        DerivedMessage(msg)


def test_base_var_len_expected_size():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg1 = b"\x00\x05hello"
    msg2 = b"\x00\x0ahelloworld"

    cmd1 = DerivedMessage(msg1)
    cmd2 = DerivedMessage(msg2)

    assert cmd1.get_expected_size() == len(msg1)
    assert cmd2.get_expected_size() == len(msg2)


def test_base_var_len_format_len_gt_msg_size():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg1 = b"\x00\x0ahello"

    with pytest.raises(Errors.OutOfBoundError):
        DerivedMessage(msg1)


def test_base_var_len_format_zero_len():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg1 = b"\x00\x00hello"
    cmd = DerivedMessage(msg1)
    assert cmd.len == 0
    assert cmd.var_len_field == b""
    assert cmd.get_expected_size() == 2


def test_base_var_len_format_len_less_than_var_len_var():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg1 = b"\x00\x04hello"
    cmd = DerivedMessage(msg1)

    assert cmd.len == 4
    assert cmd.var_len_field == b"hell"
    assert cmd.get_expected_size() == 6


def test_base_empty_msg_while_valid_format():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg1 = b""
    with pytest.raises(Errors.MessageArgError):
        DerivedMessage(msg1)


def test_base_empty_fixed_size_format_while_valid_msg():
    with pytest.raises(Errors.EmptyFormatError):

        class BaseMessage(ByteStructureBase):
            len = Field("")


def test_base_invalid_format_fixed_size():
    class BaseMessage(ByteStructureBase):
        len = Field("V")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg1 = b"\x00\x04hello"
    with pytest.raises(struct.error, match="bad char in struct format"):
        DerivedMessage(msg1)


def test_base_invalid_format_var_len_size():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: "V")

    msg1 = b"\x00\x04hello"
    with pytest.raises(struct.error, match="bad char in struct format"):
        DerivedMessage(msg1)


def test_base_invalid_field_type():
    class BaseMessage(ByteStructureBase):
        len = ">H"

    msg1 = b"\x00\x05"
    with pytest.raises(Errors.NoFieldsParsedError):
        BaseMessage(msg1)


def test_base_no_fields_present():
    class BaseMessage(ByteStructureBase): ...

    msg1 = b"\x00\x05"
    with pytest.raises(Errors.NoFieldsParsedError):
        BaseMessage(msg1)


def test_base_out_of_bond_with_fixed_size_formats():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")
        var2 = Field(">H")

    msg1 = b"\x00\x05"
    with pytest.raises(Errors.OutOfBoundError):
        BaseMessage(msg1)


def test_base_deleted_fields():
    class BaseMessage(ByteStructureBase):
        var1 = Field(">H")
        var2 = Field(">H")

    msg1 = b"\x00\x05\x00\x04"
    cmd = BaseMessage(msg1)
    assert cmd.var1 == 5
    assert cmd.var2 == 4

    del cmd.var1
    assert cmd.var2 == 4
    with pytest.raises(AttributeError, match="seems to have already been deleted"):
        cmd.var1
    assert "var1" not in cmd.parsed_fields_map
    assert msg1 == cmd.get_raw()


def test_base_precondition_for_get_size():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    msg1 = b"\x00\x05hello"
    cmd = DerivedMessage(msg1)

    cmd._ByteStructureBase__flags = 0

    with pytest.raises(
        Errors.FailedPreconditionError, match="Required flag 0x01 but 0x00 set"
    ):
        cmd.get_expected_size()

    with pytest.raises(
        Errors.FailedPreconditionError, match="Required flag 0x01 but 0x00 set"
    ):
        str(cmd)

    with pytest.raises(
        Errors.FailedPreconditionError, match="Required flag 0x01 but 0x00 set"
    ):
        cmd.get_raw()

    cmd.get_fields_and_their_names()


def test_parse_bytes_from_fields():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    cmd = DerivedMessage(parsed_fields_map=dict(len=5, var_len_field=b"hello"))
    assert cmd.len == 5
    assert cmd.var_len_field == b"hello"
    assert cmd.get_raw() == b"\x00\x05hello"


def test_parse_bytes_from_fields_when_msg_and_fields_set_or_not_set():
    class BaseMessage(ByteStructureBase):
        len = Field(">H")

    class DerivedMessage(BaseMessage):
        var_len_field = Field(lambda self: f">{self.len}s")

    with pytest.raises(
        Errors.MessageArgError,
        match="Either msg or parsed_fields_map should be provided. Not both.",
    ):
        DerivedMessage(
            b"\x00\x05hello", parsed_fields_map=dict(len=5, var_len_field=b"hello")
        )

    with pytest.raises(
        Errors.MessageArgError,
        match="Either msg or parsed_fields_map should be provided. Not both.",
    ):
        DerivedMessage()


def test_byte_structure_base_class_cannot_be_instantiated():
    with pytest.raises(TypeError, match="cannot be instantiated directly"):
        ByteStructureBase()
