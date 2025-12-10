# ocr_pipeline/pii_detector.py
import re
from typing import List, Dict
import spacy

# load spaCy model (ensure installed)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    # helpful error for user
    raise RuntimeError("spacy model en_core_web_sm not found. Run: python -m spacy download en_core_web_sm") from e

# deterministic regex patterns
PHONE_RE = re.compile(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?){1,3}\d{3,4}')
EMAIL_RE = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
SSN_RE = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')  # US SSN pattern
DATE_RE = re.compile(r'\b(?:\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}|\d{4}-\d{1,2}-\d{1,2})\b')

def regex_pii(text: str):
    matches = []
    for m in EMAIL_RE.finditer(text):
        matches.append({'type': 'EMAIL', 'text': m.group(), 'span': m.span()})
    for m in PHONE_RE.finditer(text):
        matches.append({'type': 'PHONE', 'text': m.group(), 'span': m.span()})
    for m in SSN_RE.finditer(text):
        matches.append({'type': 'SSN', 'text': m.group(), 'span': m.span()})
    for m in DATE_RE.finditer(text):
        matches.append({'type': 'DATE', 'text': m.group(), 'span': m.span()})
    return matches

def spacy_pii(text: str):
    doc = nlp(text)
    ents = []
    for ent in doc.ents:
        # choose labels relevant for PII
        if ent.label_ in ('PERSON', 'GPE', 'ORG', 'NORP'):
            ents.append({'type': ent.label_, 'text': ent.text, 'span': (ent.start_char, ent.end_char)})
    return ents

def detect_pii(text: str):
    """
    Returns list of entities with 'type', 'text', and 'span' (start,end).
    """
    results = regex_pii(text) + spacy_pii(text)
    results = sorted(results, key=lambda x: x['span'][0])
    return results
