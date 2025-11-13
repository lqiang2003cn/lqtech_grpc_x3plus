from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SingleJointPositionRequest(_message.Message):
    __slots__ = ("joint_name", "joint_value")
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    JOINT_VALUE_FIELD_NUMBER: _ClassVar[int]
    joint_name: str
    joint_value: int
    def __init__(self, joint_name: _Optional[str] = ..., joint_value: _Optional[int] = ...) -> None: ...

class ResultResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class JointPosititonArray(_message.Message):
    __slots__ = ("joint_array",)
    JOINT_ARRAY_FIELD_NUMBER: _ClassVar[int]
    joint_array: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, joint_array: _Optional[_Iterable[int]] = ...) -> None: ...
