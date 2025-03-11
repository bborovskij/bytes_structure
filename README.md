
# bytes-structure

bytes-structure is a Python library that allows you to conveniently define and parse binary protocols and their messages. It supports protocol versioning, enabling you to add new fields with each version while maintaining backward compatibility.



## Features

- **Simple and Small**: A minimal implementation focusing on simplicity and ease of use.
- **Based on Stdlib with no 3rd party packages**
- **Based on stdlib Structure Formats**: Uses Python's standard struct format strings, making it familiar to those already accustomed to these formats.
- **Easy Protocol Definition**: Define binary protocols using intuitive Python classes and Field descriptors.
- **Fixed and Variable-Length Fields**: Supports both fixed-size and variable-size fields, including those dependent on previous fields.
- **Protocol Versioning**: Extend protocols with new fields in newer versions using class inheritance.
- **Serialization and Deserialization**: Pack structured data into raw bytes and unpack raw bytes into structured data.
- **Robust Error Handling**: Comprehensive error checking and exceptions for reliable protocol parsing.


## Installation

1. From PyPi

```bash
  pip install bytes-structure
```
2. From GitHub with editor's mode
```bash
  git clone https://github.com/bborovskij/bytes_structure.git
  cd bytes_structure/
  pip install -e .
```

## Usage/Examples

### Defining Protocols
Define your binary protocol by creating a class that inherits from ByteStructureBase and declaring Field attributes.
Field's format is defined using standard Python [struct format strings](https://docs.python.org/3/library/struct.html#format-characters), ensuring familiarity and ease of use.

```python
from bytes_structure import ByteStructureBase, Field

class ProtocolV1(ByteStructureBase):
    ver = Field('>B')      # Big-endian unsigned char (1 byte)
    word1 = Field('>5s')   # Big-endian 5-byte string

```
Extend your protocol for new versions by subclassing and adding new fields:

```python
class ProtocolV2(ProtocolV1):
    length = Field('>B')                            # Big-endian unsigned char (1 byte)
    word2 = Field(lambda self: f'>{self.length}s')  # Big-endian string of variable length

```

### Creating Messages

#### Option 1: From Field Values
Create a message by providing a dictionary of field values. ByteStructure handles packing these values into raw bytes using the specified struct formats.

```python
# For Protocol V1
message_v1 = ProtocolV1(fields_map={'ver': 1, 'word1': b'hello'})
print(message_v1)            # Outputs the structured fields
print(message_v1.get_raw())  # Outputs raw bytes: b'\x01hello'

```
```python
# For Protocol V2
message_v2 = ProtocolV2(fields_map={
    'ver': 1,
    'word1': b'hello',
    'length': 5,
    'word2': b'world'
})
print(message_v2)
print(message_v2.get_raw())  # Outputs raw bytes: b'\x01hello\x05world'

```

#### Option 2: From Raw Bytes

Create a message by parsing raw bytes. ByteStructure unpacks the raw bytes into structured fields using the specified struct formats.

```python
# For Protocol V1
raw_data_v1 = b'\x01hello'
parsed_message_v1 = ProtocolV1(raw_data_v1)
print(parsed_message_v1)
print(parsed_message_v1.get_raw())  # Outputs raw bytes: b'\x01hello'

```
```python
# For Protocol V2
raw_data_v2 = b'\x01hello\x05world'
parsed_message_v2 = ProtocolV2(raw_data_v2)
print(parsed_message_v2)
print(parsed_message_v2.get_raw())  # Outputs raw bytes: b'\x01hello\x05world'

```

#### Complete Example
See examples/hello_world.

```python
from bytes_structure import ByteStructureBase, Field

class ProtocolV1(ByteStructureBase):
    ver = Field('>B')      # 1 byte
    word1 = Field('>5s')   # 5 bytes

class ProtocolV2(ProtocolV1):
    length = Field('>B')   # 1 byte
    word2 = Field(lambda self: f'>{self.length}s')  # Variable length field

# Creating a message using field values
message_v2 = ProtocolV2(fields_map={
    'ver': 1,
    'word1': b'hello',
    'length': 5,
    'word2': b'world'
})
print(message_v2.ver)         # Outputs: 1
print(message_v2.word1)       # Outputs: b'hello'
print(message_v2.length)      # Outputs: 5
print(message_v2.word2)       # Outputs: b'world'
print(message_v2.get_raw())   # Outputs: b'\x01hello\x05world'

# Parsing a message from raw bytes
raw_data = b'\x01hello\x05world'
parsed_message = ProtocolV2(raw_data)
print(parsed_message.ver)     # Outputs: 1
print(parsed_message.word1)   # Outputs: b'hello'
print(parsed_message.length)  # Outputs: 5
print(parsed_message.word2)   # Outputs: b'world'

```

## Goals

ByteStructure aims to:

- **Conveniently Define Binary Protocols**: Simplify the definition of binary messages with an intuitive and declarative approach, keeping the implementation simple and minimal.
- **Leverage Well-Known Formats**: Utilize Python's built-in struct module and familiar format strings, ensuring ease of understanding and use.
- **Support Protocol Versioning**: Enable protocols to evolve by adding new fields in new versions without breaking compatibility with older versions.

## Why ByteStructure?

- **Simplicity**: With a minimal codebase, ByteStructure focuses on making binary protocol handling as straightforward as possible.
- **Familiarity**: By using Python's standard struct format strings, you don't need to learn any new syntax or conventions.
- **Flexibility**: Supports both fixed and variable-length fields, making it suitable for a wide range of binary protocols.
- **Extensibility**: Easily extend existing protocols by subclassing and adding new fields.
## License

This project is licensed under the MIT License.
See [MIT](https://choosealicense.com/licenses/mit/).


## Contributing

TBD. Not supported at the moment.


## Acknowledgements

 - Inspired by the need for a flexible yet simple way to handle binary protocols in Python.
 - Built upon Python's built-in struct module for reliable and efficient binary data handling.
