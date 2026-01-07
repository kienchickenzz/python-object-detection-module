from pydantic import Field

from src.detector.dto.res.ResponseBase import ResponseBase
from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum

class ObjectCountResponse(ResponseBase):
    object_type: DetectableObjectEnum = Field(title="Object type")
    object_count: int = Field(title="Number of times found in the image")
