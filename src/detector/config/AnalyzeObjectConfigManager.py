from uuid import UUID

from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum
from src.detector.dto.config.ObjectAnalysisConfigRequest import ObjectAnalysisConfigRequest
from src.detector.dto.config.ObjectAnalysisConfigResponse import ObjectAnalysisConfigResponse
from src.detector.dto.ImageResolution import ImageResolution
from src.detector.dto.PixelCoordinate import PixelCoordinate
from src.detector.interface.AbstractAnalyzeImageConfigManager import AbstractAnalyzeImageConfigManager


class AnalyzeObjectConfigManager(AbstractAnalyzeImageConfigManager[ObjectAnalysisConfigRequest, ObjectAnalysisConfigResponse]):

    def __init__(
        self,
        frame_mask_repository: FrameMaskRepository,
        object_repository: ObjectRepository,
        object_analysis_config_repository: ObjectAnalysisConfigRepository
    ):
        self._frame_mask_repository = frame_mask_repository
        self._object_repository = object_repository
        self._object_analysis_config_repository = object_analysis_config_repository

    async def add_config(self, request: ObjectAnalysisConfigRequest) -> ObjectAnalysisConfigResponse:
        object_analysis_config = await self._object_analysis_config_repository.create(
            values={
                "config_name": request.config_name,
                "image_resolution_width": request.image_resolution.width,
                "image_resolution_height": request.image_resolution.height,
                "confidence": request.confidence,
            }
        )

        objects: list[DetectableObjectEnum] = []
        for request_object in request.objects:
            object = await self._object_repository.create(
                values={
                    "value": request_object,
                    "object_analysis_config": object_analysis_config.id
                }
            )
            objects.append(DetectableObjectEnum(object.value))

        image_mask: list[PixelCoordinate] = []
        if request.image_mask:
            for pixel_coordinate in request.image_mask:
                coordinate = await self._frame_mask_repository.create(
                    values={
                        "pixel_width": pixel_coordinate.width,
                        "pixel_height": pixel_coordinate.height,
                        "object_analysis_config": object_analysis_config.id
                    }
                )
                image_mask.append(
                    PixelCoordinate(
                        width=coordinate.pixel_width,
                        height=coordinate.pixel_height
                    )
                )
        
        return ObjectAnalysisConfigResponse(
            id=object_analysis_config.id,
            confidence=object_analysis_config.confidence,
            image_resolution=ImageResolution(
                width=object_analysis_config.image_resolution_width,
                height=object_analysis_config.image_resolution_height
            ),
            image_mask=image_mask if image_mask else None,
            objects=objects,
            config_name=object_analysis_config.config_name
        )
    
    async def get_config(self, config_id: UUID) -> ObjectAnalysisConfigResponse:
        frame_mask_points = await self._frame_mask_repository.get_by_object_analysis_id(
            object_analysis_config_id=config_id
        )
        objects = await self._object_repository.get_by_object_analysis_id(
            object_analysis_config_id=config_id
        )
        try:
            object_analysis_config = await self._object_analysis_config_repository.get_one(
                entity_id=config_id
            )
        except Exception as err:
            raise Exception(f"entity_{err.entity_id}_not_found_in_{err.table_name}")
        
        return ObjectAnalysisConfigResponse(
            id=object_analysis_config.id,
            config_name=object_analysis_config.config_name,
            image_resolution=ImageResolution(
                width=object_analysis_config.image_resolution_width,
                height=object_analysis_config.image_resolution_height
            ),
            confidence=object_analysis_config.confidence,
            image_mask=[
                PixelCoordinate(width=mask.pixel_width,height=mask.pixel_height) for mask in frame_mask_points
            ] if frame_mask_points else None,
            objects=[
                DetectableObjectEnum(object.value) for object in objects
            ],
        )
    
    async def get_all_configs(self) -> list[ObjectAnalysisConfigResponse]:
        object_analysis_configs = await self._object_analysis_config_repository.get_all()

        configurations: list[ObjectAnalysisConfigResponse] = []
        for config in object_analysis_configs:
            frame_mask_points = await self._frame_mask_repository.get_by_object_analysis_id(
                object_analysis_config_id=config.id
            )
            objects = await self._object_repository.get_by_object_analysis_id(
                object_analysis_config_id=config.id
            )

            configurations.append(
                ObjectAnalysisConfigResponse(
                    id=config.id,
                    config_name=config.config_name,
                    confidence=config.confidence,
                    image_resolution=ImageResolution(
                        width=config.image_resolution_width,
                        height=config.image_resolution_height
                    ),
                    image_mask=[
                        PixelCoordinate(width=mask.pixel_width,height=mask.pixel_height) for mask in frame_mask_points
                    ] if frame_mask_points else None,
                    objects=[
                        DetectableObjectEnum(object.value) for object in objects
                    ],
                )
            )
        
        return configurations
    
    async def update_config(self, config_id: UUID, request: ObjectAnalysisConfigRequest) -> ObjectAnalysisConfigResponse:
        try:
            object_analysis_config = await self._object_analysis_config_repository.get_one(entity_id=config_id)

            # delete old entities and add new
            await self._frame_mask_repository.delete_by_object_analysis_id(object_analysis_config_id=config_id)
            image_mask: list[PixelCoordinate] = []
            if request.image_mask:
                for pixel_coordinate in request.image_mask:
                    coordinate = await self._frame_mask_repository.create(
                        values={
                            "pixel_width": pixel_coordinate.width,
                            "pixel_height": pixel_coordinate.height,
                            "object_analysis_config": config_id
                        }
                    )
                    image_mask.append(
                        PixelCoordinate(
                            width=coordinate.pixel_width,
                            height=coordinate.pixel_height
                        )
                    )

            await self._object_repository.delete_by_object_analysis_id(object_analysis_config_id=config_id)      
            objects: list[DetectableObjectEnum] = []
            for request_object in request.objects:
                object = await self._object_repository.create(
                    values={
                        "value": request_object,
                        "object_analysis_config": config_id
                    }
                )
                objects.append(DetectableObjectEnum(object.value))

            updated_object_analysis_config = await self._object_analysis_config_repository.update(
                entity_id=config_id,
                values={
                    "image_resolution_width": request.image_resolution.width,
                    "image_resolution_height": request.image_resolution.height,
                    "confidence": request.confidence,
                    "config_name": request.config_name,
                }
            )
        except Exception as err:
            raise Exception(f"entity_{err.entity_id}_not_found_in_{err.table_name}")

        return ObjectAnalysisConfigResponse(
            id=updated_object_analysis_config.id,
            config_name=updated_object_analysis_config.config_name,
            confidence=updated_object_analysis_config.confidence,
            image_resolution=ImageResolution(
                width=updated_object_analysis_config.image_resolution_width,
                height=updated_object_analysis_config.image_resolution_height
            ),
            image_mask=image_mask if image_mask else None,
            objects=objects,
        )
    
    async def delete_config(self, config_id: UUID) -> None:
        try:
            object_analysis_config = await self._object_analysis_config_repository.get_one(entity_id=config_id)
            await self._object_analysis_config_repository.delete(entity_id=config_id)
        except Exception as err:
            raise Exception(f"entity_{err.entity_id}_not_found_in_{err.table_name}")
