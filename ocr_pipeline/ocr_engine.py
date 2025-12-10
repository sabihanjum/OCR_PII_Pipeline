# ocr_pipeline/ocr_engine.py
import easyocr
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from typing import List, Dict
import numpy as np
import cv2

# Initialize EasyOCR reader once. Set gpu=True if you have GPU & CUDA.
_reader = easyocr.Reader(['en'], gpu=False)

def easyocr_read(img):
    """
    img: numpy array (grayscale or color)
    returns: list of dicts: {'bbox': [[x,y],...4], 'text': str, 'conf': float}
    """
    print(f"Image shape: {img.shape}, dtype: {img.dtype}")
    results = _reader.readtext(img, detail=1)  # (bbox, text, conf)
    print(f"EasyOCR found {len(results)} text regions")
    out = []
    for bbox, text, conf in results:
        print(f"Text: '{text}', Confidence: {conf}")
        # Convert numpy arrays to regular Python lists for JSON serialization
        bbox_list = [[float(x), float(y)] for x, y in bbox]
        out.append({'bbox': bbox_list, 'text': text, 'conf': float(conf)})
    return out

def pytesseract_read(img):
    """
    Uses pytesseract.image_to_data to return word-level boxes.
    returns: list of dicts: {'bbox': [(x,y),(x2,y2)...], 'text': str, 'conf': float}
    """
    config = '--psm 6'  # assume a block of text; tune for your layout
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=config)
    out = []
    n = len(data['text'])
    for i in range(n):
        text = data['text'][i].strip()
        if text == '':
            continue
        try:
            conf = float(data['conf'][i])
        except Exception:
            conf = None
        x, y, w, h = int(data['left'][i]), int(data['top'][i]), int(data['width'][i]), int(data['height'][i])
        bbox = [(x,y), (x+w,y), (x+w,y+h), (x,y+h)]
        out.append({'bbox': bbox, 'text': text, 'conf': conf})
    return out

def hybrid_ocr(img_cv2):
    """
    Try EasyOCR first. If it returns nothing, fallback to pytesseract.
    Argument img_cv2: numpy array (BGR or grayscale)
    """
    # EasyOCR accepts either color or grayscale arrays
    easy = easyocr_read(img_cv2)
    if len(easy) > 0:
        return easy
    # fallback to Tesseract - disabled for now since Tesseract is not installed
    print("Warning: EasyOCR returned no results and Tesseract fallback is disabled")
    return []
