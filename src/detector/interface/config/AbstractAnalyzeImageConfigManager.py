from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.detector.dto.config.ImageAnalysisConfigBaseResponse import ImageAnalysisConfigBaseResponse


RESPONSE = TypeVar("RESPONSE", bound=ImageAnalysisConfigBaseResponse)

class AbstractAnalyzeImageConfigManager(ABC, Generic[RESPONSE]):

    @abstractmethod
    def get_config(self) -> RESPONSE:
        raise NotImplementedError()