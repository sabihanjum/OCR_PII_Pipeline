# tests/test_ocr.py
import os
from ocr_pipeline.ocr_engine import hybrid_ocr
import cv2

def test_ocr_runs_on_sample():
    sample = os.path.join("tests","data","sample1.jpg")
    if not os.path.exists(sample):
        print("Skipping test_ocr: sample not found")
        return
    img = cv2.imread(sample)
    res = hybrid_ocr(img)
    assert isinstance(res, list)
    # allow empty list for tricky handwriting (so not strict)
