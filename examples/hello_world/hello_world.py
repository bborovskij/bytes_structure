# MIT License
#
# Copyright (c) 2024 Bohdan Borovskyi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from bytes_structure import ByteStructureBase, Field

class ProtocolV1(ByteStructureBase):
    # https://docs.python.org/3/library/struct.html#format-characters
    # Only fixed-size fields
    ver = Field('>B')  # 1 byte
    word1 = Field('>5s')  # 5 bytes


class ProtocolV2(ProtocolV1):
    len = Field('>B')  # 1 byte
    word2 = Field(lambda self: f'>{self.len}s')  # "len" bytes long data


# Option 1: create message by providing fields_map
first_message_v1 = ProtocolV1(fields_map={'ver': 1, 'word1': b'hello'})
print(0, first_message_v1)
print(1, first_message_v1.ver, first_message_v1.word1)
print(2, f'Raw first_message_v1: {first_message_v1.get_raw()}')

first_message_v2 = ProtocolV2(fields_map={'ver': 1, 'word1': b'hello', 'len': 5, 'word2': b'world'})
print(3, first_message_v2)
print(4, first_message_v2.ver, first_message_v2.word1, first_message_v2.len, first_message_v2.word2)
print(5, f'Raw first_message_v2: {first_message_v1.get_raw()}')

# Option 2: create message by providing raw bytes
second_message_v1 = ProtocolV1(b'\x01hello')
print(6, second_message_v1)
print(7, second_message_v1.ver, second_message_v1.word1)
print(8, f'Raw second_message_v1: {second_message_v1.get_raw()}')

second_message_v2 = ProtocolV2(b'\x01hello\x05world_with_dummy_data_that_wont_be_parsed')
print(9, second_message_v2)
# note that "second_message_v2.word2" will be b'world' only since we specify its len as 5
print(10, second_message_v2.ver, second_message_v2.word1, second_message_v2.len, second_message_v2.word2)
# entire message will be printed
print(11, f'Raw second_message_v2: {second_message_v2.get_raw()}')
