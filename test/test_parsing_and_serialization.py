import string
from random import choices

import pytest

from bytes_structure import ByteStructureBase, Field, Errors


@pytest.fixture
def ProtocolVarLenV1():
    class _Proto(ByteStructureBase):
        len = Field(">B")
        word = Field(lambda self: f">{self.len}s")

    return _Proto


@pytest.mark.parametrize("msg_len", [0, 1, 10, 0xFF])
def test_protocol_parsing_positive(msg_len, ProtocolVarLenV1):
    """
    Test that different length message can be parsed.
    """
    word = "".join(choices(string.ascii_uppercase + string.digits, k=msg_len)).encode()
    msg = ProtocolVarLenV1(bytes([msg_len]) + word)
    assert msg.len == msg_len
    assert len(msg.word) == msg_len
    assert msg.word == word


@pytest.mark.parametrize("msg_len", [0, 1, 10, 0xFF])
def test_protocol_serialization_positive(msg_len, ProtocolVarLenV1):
    """
    Test that different length message can be serialized.
    """
    word = "".join(choices(string.ascii_uppercase + string.digits, k=msg_len)).encode()
    msg = ProtocolVarLenV1(fields_map={"len": msg_len, "word": word})
    assert msg.len == msg_len
    assert len(msg.word) == msg_len
    assert msg.word == word


@pytest.mark.parametrize("msg_len", [1, 10, 0xFF])
def test_protocol_parsing_out_of_bond_len(msg_len, ProtocolVarLenV1):
    """
    Test that ProtocolVarLenV1 obj can handle bytes data when length is larger than var. length message.
    """
    word = "".join(
        choices(string.ascii_uppercase + string.digits, k=msg_len - 1)
    ).encode()
    with pytest.raises(
        Errors.OutOfBoundError,
        match="Going out of bonds or incorrect endianness for len in case of var len field",
    ):
        ProtocolVarLenV1(bytes([msg_len]) + word)


@pytest.mark.parametrize("msg_len", [1, 10, 0xFF])
def test_protocol_serialization_out_of_bond_len(msg_len, ProtocolVarLenV1):
    """
    Test that ProtocolVarLenV1 obj can handle values from fields map when length is larger than var. length message.
    """
    word = "".join(
        choices(string.ascii_uppercase + string.digits, k=msg_len - 1)
    ).encode()
    with pytest.raises(
        Errors.OutOfBoundError,
        match="Going out of bonds or incorrect endianness for len in case of var len field",
    ):
        ProtocolVarLenV1(fields_map={"len": msg_len, "word": word})


@pytest.mark.parametrize(
    "fmt,msg_len",
    [
        (">B", 0x0100),
        (">B", -1),
        (">H", 0x10000),
        (">H", -1),
    ],
)
def test_serialization_when_incorrect_data_for_format(fmt, msg_len):
    word = "".join(choices(string.ascii_uppercase + string.digits, k=msg_len)).encode()

    class Protocol(ByteStructureBase):
        len = Field(fmt)
        data = Field(lambda self: f">{self.len}s")

    with pytest.raises(Errors.PackError, match="Error packing"):
        Protocol(fields_map={"len": msg_len, "data": word})


@pytest.mark.parametrize(
    "fmt,msg_len",
    [
        (">B", -1),
        (">H", -1),
    ],
)
def test_serialization_with_negative_len(fmt, msg_len):
    class Protocol(ByteStructureBase):
        len = Field(fmt)

    with pytest.raises(Errors.PackError, match="Error packing"):
        Protocol(fields_map={"len": msg_len})


def test_serialization_with_incorrect_field_name():
    class Protocol(ByteStructureBase):
        len = Field(">B")
        data = Field(">B")

    with pytest.raises(
        Errors.FieldNameError,
        match="Provided field names on init must be equal to field names from Field class attributes",
    ):
        Protocol(fields_map={"length": 1})

    with pytest.raises(
        Errors.FieldNameError,
        match="Provided field names on init must be equal to field names from Field class attributes",
    ):
        Protocol(fields_map={"len": 1})
