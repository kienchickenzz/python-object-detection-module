import numpy as np
from cv2 import rectangle, putText, FONT_HERSHEY_SIMPLEX

from src.detector.dto.res.ObjectLocationResponse import ObjectLocationResponse


class BoundingBoxVisualizer:
    """Chịu trách nhiệm duy nhất: vẽ bounding box lên ảnh"""
    
    def __init__(
        self,
        thickness: int = 3,
        color: tuple[int, ...] = (255, 0, 255),
        font_scale: float = 1.0
    ):
        self._thickness = thickness
        self._color = color
        self._font_scale = font_scale
    
    def draw(
        self,
        image: np.ndarray,
        bounding_boxes: list[ObjectLocationResponse],
        make_copy: bool = False,
        include_label: bool = True
    ) -> np.ndarray:
        canvas = image.copy() if make_copy else image
        
        for box in bounding_boxes:
            rectangle(
                img=canvas,
                pt1=(box.top_left.width, box.top_left.height),
                pt2=(box.bottom_right.width, box.bottom_right.height),
                color=self._color,
                thickness=self._thickness
            )
            
            if include_label:
                text = f"{box.object_type.value}:{box.confidence}"
                putText(
                    img=canvas,
                    text=text,
                    org=(box.top_left.width, box.top_left.height),
                    fontFace=FONT_HERSHEY_SIMPLEX,
                    fontScale=self._font_scale,
                    color=self._color,
                    thickness=self._thickness
                )
        
        return canvas