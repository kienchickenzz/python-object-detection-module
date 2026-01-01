from pydantic import Field

from src.detector.dto.Base import Base
from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum
from src.detector.dto.PixelCoordinate import PixelCoordinate


class ObjectBoundingBox(Base):
    object_type: DetectableObjectEnum = Field(title="Object type")
    confidence: float = Field(title="Object detection confidence in percentage")
    top_left: PixelCoordinate = Field(title="Top-left corner of bounding box")
    bottom_right: PixelCoordinate = Field(title="Bottom-right corner of bounding box")
