from abc import ABC, abstractmethod
from typing import Optional

from numpy import ndarray

from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum
from src.detector.dto.ObjectBoundingBox import ObjectBoundingBox


class AbstractObjectDetector(ABC):
    """
    Contract cho tất cả object detectors
    - Cho phép swap algorithms (YOLOv8, YOLOv9, Faster R-CNN, etc.)
    """

    @abstractmethod
    def count(
        self, 
        image: ndarray, 
        objects: list[DetectableObjectEnum],
        confidence: Optional[float] = None
    ) -> dict[DetectableObjectEnum, int]:
        """
        Đếm số lượng objects trong ảnh

        Args:
            image: Numpy array của ảnh (đã qua preprocessing)
            objects: List các ObjectEnum cần detect (car, bus, motorbike...)
            confidence: Ngưỡng confidence (0-100), override default

        Returns:
            {ObjectEnum.CAR: 5, ObjectEnum.BUS: 2, ...}
        """
        raise NotImplementedError()

    @abstractmethod
    def detect(
        self, 
        image: ndarray, 
        objects: list[DetectableObjectEnum],
        confidence: Optional[float] = None
    ) -> dict[DetectableObjectEnum, list[ObjectBoundingBox]]:
        """
        Detect objects và trả về bounding boxes

        Returns:
            {
                ObjectEnum.CAR: [
                    ObjectBoundingBox(top_left=(10,20), bottom_right=(50,60), confidence=95),
                    ...
                ]
            }
        """
        raise NotImplementedError()
