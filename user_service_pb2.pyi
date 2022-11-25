from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DBUserResponse(_message.Message):
    __slots__ = ["data", "message", "status"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    data: UserDataDict
    message: str
    status: bool
    def __init__(self, status: bool = ..., message: _Optional[str] = ..., data: _Optional[_Union[UserDataDict, _Mapping]] = ...) -> None: ...

class UserDataDict(_message.Message):
    __slots__ = ["email", "password", "role", "username"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    password: str
    role: str
    username: str
    def __init__(self, username: _Optional[str] = ..., email: _Optional[str] = ..., role: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...
