OCR + PII Extraction Pipeline

Lightweight, end-to-end pipeline to extract text from scanned or handwritten images, detect personally identifiable information (PII), and optionally redact detected PII in the image. Includes a visual debug web UI, CLI, and REST API.

Features

Hybrid OCR engine — EasyOCR primary with Tesseract fallback

PII detection — Regex patterns + spaCy NER (emails, phones, dates, SSN-like, PERSON/ORG/GPE)

Preprocessing — deskewing, denoising, adaptive thresholding, resizing profiles

Redaction — draw solid boxes over PII regions on images

Debug Web UI — upload, preview OCR boxes, compare preprocessing, view/save runs (gallery)

CLI & REST API — programmatic usage for batch or service workflows


Quickstart (Windows / Linux / macOS)
1. Create and activate a virtual environment

Windows (PowerShell)

python -m venv venv
.\venv\Scripts\Activate.ps1


Linux / macOS

python3 -m venv venv
source venv/bin/activate

2. Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt


If spaCy model does not install automatically:

python -m spacy download en_core_web_sm

3. Install Tesseract (fallback engine)

Windows: download UB-Mannheim build and ensure tesseract.exe is on PATH.
Linux: sudo apt install tesseract-ocr (or your distro package manager).

Verify:

tesseract --version

Usage
CLI
python -m ocr_pipeline.cli samples/sample1.jpg \
  --out output.json \
  --redact \
  --redacted-out sample1_redacted.jpg


Outputs

output.json — OCR tokens + PII detections

sample1_redacted.jpg — image with redaction boxes

sample1.jpg.proc.jpg — preprocessed image used for OCR

REST API

Start the server:

python -m ocr_pipeline.api


Server default URL:

http://127.0.0.1:5000/


Process programmatically

curl.exe -X POST -F image=@samples/sample1.jpg http://127.0.0.1:5000/process

Debug Web UI

Open in your browser:

http://127.0.0.1:5000/debug


Capabilities:

Upload an image and view OCR overlays

Toggle PII-only display and confidence labels

Compare Original / Preprocessed / Resized previews

Save runs to gallery for download and inspection

Tests

Place sample test images under tests/data/ if needed, then:

pytest -q


If pytest fails to import the package, run tests with the project on PYTHONPATH:

# PowerShell
$env:PYTHONPATH = (Get-Location).Path
pytest -q


Or install the package in editable mode once:

pip install -e .
pytest -q

Implementation notes & tips

Pipeline flow:
Input (JPEG) → Preprocessing → OCR (EasyOCR → Tesseract fallback) → Text cleaning → PII detection → (optional) image redaction

Improve OCR quality:

Upsample images (cv2.resize) before OCR

Tune preprocessing (adaptive threshold params, denoising)

Use spell-correction or an LM to merge fragmented tokens

Consider handwriting-specialized models (TrOCR, Donut) for difficult handwriting

EasyOCR compatibility: prefer Pillow ≤ 9.5.0 if EasyOCR raises Image.ANTIALIAS errors. You can also add a small monkeypatch to map Image.ANTIALIAS to Image.Resampling.LANCZOS on Pillow 10+.

Security & production:

Protect API endpoints with authentication/authorization

Secure stored PII (encryption at rest, limited retention)

Add audit logs for PII access and redaction events

Sanitize uploads and set size limits

Gallery & Debug Storage

Runs saved via the debug UI are stored under the system temp directory in ocr_pii_debug_gallery/ with timestamped subfolders containing:

original image, OCR JSON, redacted image, metadata

Roadmap / Enhancements

Add spell-correction + language-model post-processing

Add comparison of OCR engines (EasyOCR vs Tesseract vs TrOCR)

Provide a React front-end for UX improvements (drag & drop, progress)

Dockerize with GPU support for performance (optional)

CSV export of PII tokens for data pipelines

License & Attribution

This repository is a starter template. If you repurpose it in production, ensure compliance with any third-party license terms (EasyOCR, Tesseract, spaCy, PyTorch, etc.).
