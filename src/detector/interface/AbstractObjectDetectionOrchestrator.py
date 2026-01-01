from abc import ABC, abstractmethod

import numpy as np

from src.detector.dto.config.ObjectAnalysisConfigResponse import ObjectAnalysisConfigResponse
from src.detector.dto.res.ObjectCountResponse import ObjectCountResponse
from src.detector.dto.res.ObjectLocationResponse import ObjectLocationResponse


class AbstractObjectDetectionOrchestrator(ABC):

    @abstractmethod
    async def count_objects(
        self, 
        image_arr: np.ndarray, 
        object_analysis_config: ObjectAnalysisConfigResponse
    ) -> list[ObjectCountResponse]:
        raise NotImplementedError()
    
    @abstractmethod
    async def locate_objects(
        self, 
        image_arr: np.ndarray, 
        object_analysis_config: ObjectAnalysisConfigResponse
    ) -> list[ObjectLocationResponse]:
        raise NotImplementedError()
