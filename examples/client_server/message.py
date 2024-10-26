from bytes_structure import ByteStructureBase, Field


class MessageV1(ByteStructureBase):
    # https://docs.python.org/3/library/struct.html#format-characters
    ver = Field(">B")
    msg_id = Field(">H")
    data_len = Field(">B")
    data = Field(lambda self: f">{self.data_len}s")


class MessageV2(MessageV1):
    additional_data_len = Field(">B")
    additional_data = Field(lambda self: f">{self.additional_data_len}s")
