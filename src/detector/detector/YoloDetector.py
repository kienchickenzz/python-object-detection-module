from typing import Optional
from pathlib import Path
from math import ceil

import numpy as np
from ultralytics.models import YOLO 
from ultralytics.engine.results import Boxes, Results

from src.detector.interface.AbstractObjectDetector import AbstractObjectDetector
from src.detector.enum.DetectableObjectEnum import DetectableObjectEnum
from src.detector.dto.ObjectBoundingBox import ObjectBoundingBox
from src.detector.dto.PixelCoordinate import PixelCoordinate


class YoloDetector(AbstractObjectDetector):
    """_summary_

    Args:
        ObjectDetector (_type_): _description_

    Raises:
        AnalyzerException: _description_

    Returns:
        _type_: _description_
    """
    CLASS_NAMES = [
        "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
        "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
        "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
        "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
        "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
        "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
        "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
        "teddy bear", "hair drier", "toothbrush"
    ]

    def __init__(
            self, 
            model_path: str = f"{Path(__file__).parent.resolve()}/yolo-Weights/yolov8n.pt",
            confidence: float = 0.85
        ):
        """
        Initialize YOLO object detector.

        :param model_path: path to YoLo model, defaults to pre-trained model by 'ultralytics'
        :type model_path: str, optional
        :param confidence: default confidence level for detection, defaults 85%
        :type confidence: int, optional
        """
        self._model = YOLO(model_path)
        self._confidence = confidence
    
    def _filter_boxes(
        self, 
        boxes: list[Boxes], 
        objects: list[DetectableObjectEnum], 
        confidence: Optional[float] = None
    ) -> dict[str, list[Boxes]]:
        # if confidence not specified then use default
        conf_level = confidence if confidence else self._confidence

        # filter out only specified objects
        object_names = [object.value for object in objects]
        filtered_results: dict[str, list[Boxes]] = {object_name: [] for object_name in object_names}
        for box in boxes:
            class_name = self.CLASS_NAMES[int(box.cls[0])]
            
            if class_name in object_names and box.conf[0] >= conf_level:
                filtered_results[class_name].append(box)

        return filtered_results
    
    def count(
        self, 
        image: np.ndarray, 
        objects: list[DetectableObjectEnum], 
        confidence: Optional[float] = None
    ) -> dict[DetectableObjectEnum, int]:
        # infer objects from the image
        results: Results = self._model(image, stream=False)[0]

        # filter out only specified objects
        filtered_results = self._filter_boxes(
            boxes=results.boxes, 
            objects=objects, 
            confidence=confidence
        )
        
        # default return value
        counting_results: dict[DetectableObjectEnum, int] = {
            object: 0 for object in objects
        }

        # count objects from results
        for class_name, boxes in filtered_results.items():
            object_enum = DetectableObjectEnum(class_name)
            counting_results[object_enum] += len(boxes)

        return counting_results
    
    def detect(
        self, 
        image: np.ndarray, 
        objects: list[DetectableObjectEnum], 
        confidence: Optional[float] = None
    ) -> dict[DetectableObjectEnum, list[ObjectBoundingBox]]:
        # infer objects from the image
        results: Results = self._model(image, stream=False)[0]
        if results.boxes is None:
            raise Exception("No bounding boxes found in the results!")

        # filter out only specified objects
        filtered_results = self._filter_boxes(
            boxes=results.boxes, 
            objects=objects, 
            confidence=confidence
        )

        # default return value
        detection_results: dict[DetectableObjectEnum, list[ObjectBoundingBox]] = {
            object: [] for object in objects
        }

        # group bounding boxes by object type
        for class_name, boxes in filtered_results.items():
            object_enum = DetectableObjectEnum(class_name)

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                detection_results[object_enum] += [
                    ObjectBoundingBox(
                        object_type=object_enum,
                        confidence=ceil((box.conf[0]*100)),
                        top_left=PixelCoordinate(
                            width=int(x1),
                            height=int(y1)
                        ),
                        bottom_right=PixelCoordinate(
                            width=int(x2),
                            height=int(y2)
                        )
                    )
                ]
            
        return detection_results