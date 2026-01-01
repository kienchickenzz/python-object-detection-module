from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from src.detector.dto.config.ImageAnalysisConfigBaseRequest import ImageAnalysisConfigBaseRequest
from src.detector.dto.config.ImageAnalysisConfigBaseResponse import ImageAnalysisConfigBaseResponse


REQUEST = TypeVar("REQUEST", bound=ImageAnalysisConfigBaseRequest)
RESPONSE = TypeVar("RESPONSE", bound=ImageAnalysisConfigBaseResponse)

class AbstractAnalyzeImageConfigManager(ABC, Generic[REQUEST, RESPONSE]):

    @abstractmethod
    async def add_config(self, request: REQUEST) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_config(self, config_id: UUID) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_all_configs(self) -> list[RESPONSE]:
        raise NotImplementedError()
    
    @abstractmethod
    async def update_config(self, config_id: UUID, request: REQUEST) -> RESPONSE:
        raise NotImplementedError()
    
    @abstractmethod
    async def delete_config(self, config_id: UUID) -> None:
        raise NotImplementedError()