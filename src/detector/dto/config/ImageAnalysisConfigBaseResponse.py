from typing import Optional

from pydantic import Field

from src.shared.dto.ResponseBase import ResponseBase
from src.detector.dto.ImageResolution import ImageResolution
from src.detector.dto.PixelCoordinate import PixelCoordinate


class ImageAnalysisConfigBaseResponse(ResponseBase):
    id: int = Field(title="Analysis config ID")
    config_name: Optional[str] = Field(
        title="Configuration name", 
        default=None
    )
    image_resolution: ImageResolution = Field(
        title="Image resolution", 
        description="Resolution of the images that will be analyzed"
    )
    image_mask: Optional[list[PixelCoordinate]] = Field(
        title="Image mask", 
        description="Area on the image that will be blacked out before analysis"
    )
