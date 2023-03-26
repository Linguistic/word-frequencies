from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FrequencyDictionary(_message.Message):
    __slots__ = ["frequency", "language"]
    class FrequencyEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: int
        def __init__(self, key: Optional[str] = ..., value: Optional[int] = ...) -> None: ...
    FREQUENCY_FIELD_NUMBER: ClassVar[int]
    LANGUAGE_FIELD_NUMBER: ClassVar[int]
    frequency: _containers.ScalarMap[str, int]
    language: str
    def __init__(self, language: Optional[str] = ..., frequency: Optional[Mapping[str, int]] = ...) -> None: ...
