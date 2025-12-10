# ocr_pipeline/cli.py
import argparse
import json
import cv2
from .preprocess import enhance_for_ocr
from .ocr_engine import hybrid_ocr
from .text_cleaning import clean_text_from_ocr
from .pii_detector import detect_pii
from .redactor import redact_image_with_bboxes

def map_entities_to_bboxes(ocr_results, pii_entities):
    """
    Naive mapping: for each detected PII text, find OCR token that contains that substring.
    Returns list of bboxes (the OCR token boxes) corresponding to PII tokens.
    """
    bboxes = []
    for ent in pii_entities:
        ent_text = ent['text'].strip().lower()
        for token in ocr_results:
            token_text = token.get('text','').strip().lower()
            if ent_text and ent_text in token_text:
                bboxes.append(token['bbox'])
    return bboxes

def run_pipeline(img_path, out_json="output.json", redact=False, redact_out="redacted.jpg"):
    proc_path = img_path + ".proc.jpg"
    processed = enhance_for_ocr(img_path, save_path=proc_path)
    
    # Try both original and processed images
    print("Trying original image...")
    img_orig = cv2.imread(img_path)
    ocr_results = hybrid_ocr(img_orig)
    
    if not ocr_results:
        print("No results from original, trying processed image...")
        # read processed image for OCR (OpenCV loads as BGR)
        img_cv = cv2.imread(proc_path)
        ocr_results = hybrid_ocr(img_cv)
    
    # join OCR tokens to a single text for PII detection
    full_text = " ".join([clean_text_from_ocr(item['text']) for item in ocr_results])
    pii = detect_pii(full_text)
    bboxes = map_entities_to_bboxes(ocr_results, pii)
    out = {
        'ocr': ocr_results,
        'pii': pii,
    }
    with open(out_json, 'w') as f:
        json.dump(out, f, indent=2)
    if redact and bboxes:
        redact_image_with_bboxes(img_path, bboxes, redact_out)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OCR + PII extraction pipeline CLI")
    parser.add_argument("image", help="Path to input image (JPEG/PNG)")
    parser.add_argument("--out", default="output.json", help="JSON output path")
    parser.add_argument("--redact", action="store_true", help="Whether to save a redacted image")
    parser.add_argument("--redacted-out", default="redacted.jpg", help="Redacted image output path")
    args = parser.parse_args()
    print("Running pipeline on", args.image)
    result = run_pipeline(args.image, out_json=args.out, redact=args.redact, redact_out=args.redacted_out)
    print("Saved JSON to", args.out)
    if args.redact and result:
        print("Saved redacted image to", args.redacted_out)
