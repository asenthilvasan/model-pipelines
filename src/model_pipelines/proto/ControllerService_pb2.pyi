from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PipelineRequest(_message.Message):
    __slots__ = ("image_url", "pipeline_steps")
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_STEPS_FIELD_NUMBER: _ClassVar[int]
    image_url: str
    pipeline_steps: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, image_url: _Optional[str] = ..., pipeline_steps: _Optional[_Iterable[str]] = ...) -> None: ...

class PipelineOutput(_message.Message):
    __slots__ = ("final_image",)
    FINAL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    final_image: bytes
    def __init__(self, final_image: _Optional[bytes] = ...) -> None: ...
