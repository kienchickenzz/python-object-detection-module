from pydantic import Field

from src.detector.dto.Base import Base


class ImageResolution(Base):
    width: int = Field(title="Image width in pixels", default=1920)
    height: int = Field(title="Image height in pixels", default=1080)
