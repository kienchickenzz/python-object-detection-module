from pydantic import Field

from src.shared.dto.ResponseBase import ResponseBase
from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum

class ObjectCountResponse(ResponseBase):
    object_type: DetectableObjectEnum = Field(title="Object type")
    object_count: int = Field(title="Number of times found in the image")
