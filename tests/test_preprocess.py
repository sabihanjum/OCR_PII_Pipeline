# tests/test_preprocess.py
import os
from ocr_pipeline.preprocess import enhance_for_ocr

def test_enhance_exists():
    # expects there's a sample file at tests/data/sample1.jpg (create or place your test sample)
    sample = os.path.join("tests","data","sample1.jpg")
    if not os.path.exists(sample):
        print("Skipping test: sample not found:", sample)
        return
    out = enhance_for_ocr(sample, save_path=sample + ".proc.jpg")
    assert out is not None
    # check file saved
    assert os.path.exists(sample + ".proc.jpg")
