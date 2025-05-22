from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ImageRequest(_message.Message):
    __slots__ = ("image_data",)
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    image_data: bytes
    def __init__(self, image_data: _Optional[bytes] = ...) -> None: ...

class ImageResponse(_message.Message):
    __slots__ = ("result_image",)
    RESULT_IMAGE_FIELD_NUMBER: _ClassVar[int]
    result_image: bytes
    def __init__(self, result_image: _Optional[bytes] = ...) -> None: ...
