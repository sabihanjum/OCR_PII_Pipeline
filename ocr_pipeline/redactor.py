# ocr_pipeline/redactor.py
import cv2
import numpy as np
from typing import List

def _bbox_to_rect(bbox):
    """
    Accepts:
      - bbox as 4-point polygon: [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
      - bbox as (x, y, w, h)
    Returns: (x1,y1,x2,y2)
    """
    if isinstance(bbox, (list, tuple)) and len(bbox) == 4 and isinstance(bbox[0], (list, tuple)):
        xs = [int(p[0]) for p in bbox]
        ys = [int(p[1]) for p in bbox]
        return min(xs), min(ys), max(xs), max(ys)
    elif isinstance(bbox, (list, tuple)) and len(bbox) == 4:
        x, y, w, h = bbox
        return int(x), int(y), int(x + w), int(y + h)
    else:
        raise ValueError("Unsupported bbox format")

def redact_image_with_bboxes(img_path: str, bboxes: List, output_path: str):
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(img_path)
    for bbox in bboxes:
        x1, y1, x2, y2 = _bbox_to_rect(bbox)
        # draw filled black rectangle (modify color as needed)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,0), thickness=-1)
    cv2.imwrite(output_path, img)
    return output_path
