# File: Yolo_image_detector - This file contains a class for detecting objects in images using YOLOv8.
# It fetches images from URLs, processes them with a YOLO model, 
# and returns the images names that contains the target class with some probability.

import requests
import numpy as np
import cv2
from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="yolov8n.pt", target_class=None):
        self.model = YOLO(model_path)
        self.class_names = self.model.names  # {id: name}

        if target_class is not None:
            if target_class not in self.class_names.values():
                raise ValueError(f"'{target_class}' is not a valid class. Must be one of: {list(self.class_names.values())}")
        self.target_class = target_class  # holds one valid label (or None)

    def _load_image_from_url(self, url):
        response = requests.get(url)
        img_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img

    def detect_all(self, images):
        """
        Accepts a list of image URLs.
        Returns a list of lists, each inner list contains (label, confidence) for one image.
        """
        all_target_detections = []
        print("target class is:=",self.target_class)
        for filename, public_url in images:
            try:
                img = self._load_image_from_url(public_url)
                results = self.model(img)[0]
                

                if not results.boxes:
                    continue

                detections = []
                for box in results.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    label = results.names[class_id]
                    if label==self.target_class or self.target_class is None:
                        ##if confidence >= 0.25:
                        detections.append((label, confidence))
                if len(detections) > 0:
                    all_target_detections.append((filename,results))

            except Exception as e:
                print(f"Error processing {public_url}: {e}")
                all_target_detections.append([("error", 0.0)])


        #for filename, results in all_target_detections:  UNCOMMENT THIS TO SHOW RESULTS
           # results.show()
        return all_target_detections


#EXAMPLE MODULE USAGE
"""
if __name__ == "__main__":
    detector = YoloDetector()

    urls = [
"https://tpgyjmwkfofcibihtdhl.supabase.co/storage/v1/object/public/cats/cat.151.jpg?"    ]

    results = detector.detect_all(urls)

    for list in results:
        print(list)
"""