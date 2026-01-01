from typing import Optional

import numpy as np
from cv2 import fillPoly

from src.detector.dto.ImageResolution import ImageResolution
from src.detector.dto.PixelCoordinate import PixelCoordinate


class MaskProcessor:
    """Chịu trách nhiệm duy nhất: xử lý mask trên ảnh"""
    
    @staticmethod
    def apply_blackout(
        image_arr: np.ndarray,
        resolution: ImageResolution,
        mask: Optional[list[PixelCoordinate]]
    ) -> np.ndarray:
        if mask is None:
            return image_arr
        
        MaskProcessor._validate_mask(mask, resolution)
        
        pixels_list = [[pixel.width, pixel.height] for pixel in mask]
        mask_array = np.array(pixels_list, dtype=np.int32)
        pts = mask_array.reshape((-1, 1, 2))
        
        return fillPoly(image_arr, [pts], color=(0, 0, 0))
    
    @staticmethod
    def _validate_mask(
        mask: list[PixelCoordinate], 
        resolution: ImageResolution
    ) -> None:
        """Kiểm tra mask có nằm trong boundary của ảnh không"""
        pixels_list = [[pixel.width, pixel.height] for pixel in mask]
        mask_array = np.array(pixels_list)
        
        if mask_array.min() < 0:
            raise Exception("Mask coordinates cannot be negative")
        
        if mask_array[:, 0].max() > resolution.width:
            raise Exception("Mask exceeds image width")
        
        if mask_array[:, 1].max() > resolution.height:
            raise Exception("Mask exceeds image height")
