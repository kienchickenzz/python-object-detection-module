from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum
from src.detector.dto.config.ObjectAnalysisConfigResponse import ObjectAnalysisConfigResponse
from src.detector.dto.ImageResolution import ImageResolution
from src.detector.interface.config.AbstractAnalyzeImageConfigManager import AbstractAnalyzeImageConfigManager


class AnalyzeObjectConfigManager(AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigResponse]):

    CONFIG_ID = 1
    DEFAULT_CONFIDENCE = 0.85
    DEFAULT_RESOLUTION = ImageResolution(width=1920, height=1080)
    DEFAULT_OBJECTS = [
        DetectableObjectEnum.CAR,
        DetectableObjectEnum.MOTORBIKE,
        DetectableObjectEnum.BICYCLE,
        DetectableObjectEnum.BUS,
        DetectableObjectEnum.TRUCK,
        
        DetectableObjectEnum.PERSON,
    ]

    def get_config(self) -> ObjectAnalysisConfigResponse:
        return ObjectAnalysisConfigResponse(
            id=self.CONFIG_ID,
            config_name="Default Configuration",
            image_resolution=self.DEFAULT_RESOLUTION,
            confidence=self.DEFAULT_CONFIDENCE,
            objects=self.DEFAULT_OBJECTS,
            image_mask=None
        )
