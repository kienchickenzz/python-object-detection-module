from pydantic import Field

from src.shared.dto.ResponseBase import ResponseBase

from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum
from src.detector.dto.ObjectBoundingBox import ObjectBoundingBox
from src.detector.dto.PixelCoordinate import PixelCoordinate

class ObjectLocationResponse(ResponseBase):
    object_type: DetectableObjectEnum = Field(title="Object type")
    confidence: float = Field(title="Object detection confidence in percentage")
    top_left: PixelCoordinate = Field(title="Top-left corner of bounding box")
    bottom_right: PixelCoordinate = Field(title="Bottom-right corner of bounding box")

    @classmethod
    def from_bounding_box(cls, dto: ObjectBoundingBox) -> 'ObjectLocationResponse':
        return ObjectLocationResponse(
            object_type=dto.object_type,
            confidence=dto.confidence,
            top_left=PixelCoordinate.from_dto(dto.top_left),
            bottom_right=PixelCoordinate.from_dto(dto.bottom_right)
        )
    