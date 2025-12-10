# tests/test_pii.py
from ocr_pipeline.pii_detector import detect_pii

def test_detect_pii_basic():
    s = "Patient: John Doe\nPhone: +1-555-123-4567\nEmail: john.doe@example.com\nDOB: 03/05/1980\nSSN: 123-45-6789"
    ents = detect_pii(s)
    types = set([e['type'] for e in ents])
    assert 'EMAIL' in types
    assert 'PHONE' in types or any('555' in e['text'] for e in ents)
    assert 'SSN' in types
