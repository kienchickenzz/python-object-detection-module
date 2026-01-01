from pydantic import Field

from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum
from src.detector.dto.config.ImageAnalysisConfigBaseRequest import ImageAnalysisConfigBaseRequest


BASE_CONFIDENCE = 0.85

class ObjectAnalysisConfigRequest(ImageAnalysisConfigBaseRequest):
    confidence: float = Field(
        title="Confidence threshold", 
        description="Confidence level above which detected object is trusted to be correct (0...1.0)", 
        default=BASE_CONFIDENCE
    )
    objects: list[DetectableObjectEnum] = Field(title="Objects of interest on the image")
