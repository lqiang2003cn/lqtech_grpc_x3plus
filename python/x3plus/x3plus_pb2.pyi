from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HelloRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class SingleJointPositionRequest(_message.Message):
    __slots__ = ("joint_name", "joint_value")
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    JOINT_VALUE_FIELD_NUMBER: _ClassVar[int]
    joint_name: str
    joint_value: int
    def __init__(self, joint_name: _Optional[str] = ..., joint_value: _Optional[int] = ...) -> None: ...

class SingleJointPositionResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...
