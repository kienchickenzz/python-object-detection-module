import asyncio
from pprint import pprint

import cv2 as cv
from cv2 import IMREAD_COLOR, imdecode
from numpy import uint8, frombuffer

from src.detector.config.AnalyzeObjectConfigManager import AnalyzeObjectConfigManager
from src.detector.detector.ObjectDetectionOrchestrator import ObjectDetectionOrchestrator
from src.detector.detector.YoloDetector import YoloDetector 
from src.detector.util.BoundingBoxVisualizer import BoundingBoxVisualizer


IMAGE_PATH = './output/test_02.jpg'

async def main():

    with open(IMAGE_PATH, 'rb') as image_file:
        image_bytes = image_file.read()
    arr = frombuffer(image_bytes, uint8)
    image_arr = imdecode(arr, IMREAD_COLOR)

    analysis_config = AnalyzeObjectConfigManager()
    yolo_detector = YoloDetector(
        model_path='./weight/yolov8n.pt',
        confidence=0.5
    )
    orchestrator = ObjectDetectionOrchestrator(yolo_detector)
    result = await orchestrator.locate_objects(
        image_arr=image_arr, 
        object_analysis_config=analysis_config.get_config()
    )
    pprint(result)

    visualizer = BoundingBoxVisualizer()
    visualized_img_arr = visualizer.draw(
        image=image_arr, 
        bounding_boxes=result
    )

    cv.imwrite('./output/output.jpg', visualized_img_arr)

if __name__ == "__main__":
    asyncio.run(main())
