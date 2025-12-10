# ocr_pipeline/text_cleaning.py
import re

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def fix_common_ocr_errors(text):
    # minimal set of heuristics; expand as needed
    text = text.replace('|', 'I')
    text = text.replace('”', '"').replace('“', '"')
    text = text.replace('—', '-')
    text = text.replace('•', '-')
    text = normalize_whitespace(text)
    return text

def clean_text_from_ocr(text):
    text = fix_common_ocr_errors(text)
    return text
