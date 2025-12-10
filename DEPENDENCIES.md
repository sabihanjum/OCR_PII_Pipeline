# OCR PII Pipeline - Dependencies Documentation

## Assignment Deliverable: Dependency Document

This document lists all required dependencies for the OCR + PII Extraction Pipeline for Handwritten Documents.

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, Linux, or macOS
- **Memory**: Minimum 4GB RAM (8GB recommended for better performance)
- **Storage**: ~2GB for dependencies and models

## Python Dependencies

### Core Dependencies (requirements_win.txt)

```
opencv-python==4.8.1.78          # Computer vision and image processing
numpy==1.24.0                    # Numerical computing
pytesseract==0.3.10              # Tesseract OCR wrapper (fallback engine)
easyocr==1.6.2                   # Primary OCR engine for handwritten text
flask==2.3.2                     # Web framework for API/UI
spacy==3.6.0                     # Natural Language Processing for PII detection
pytest==7.4.0                    # Testing framework
Pillow==10.0.0                   # Image processing library
```

### Additional Dependencies (Auto-installed)

#### EasyOCR Dependencies:
- `torch` - PyTorch deep learning framework
- `torchvision` - Computer vision models
- `opencv-python-headless` - OpenCV without GUI
- `scipy` - Scientific computing
- `scikit-image` - Image processing algorithms
- `python-bidi` - Bidirectional text support
- `PyYAML` - YAML parser
- `Shapely` - Geometric operations
- `pyclipper` - Polygon clipping
- `ninja` - Build system

#### spaCy Dependencies:
- `en-core-web-sm` - English language model for NER
- `murmurhash` - Hash functions
- `cymem` - Memory management
- `preshed` - Hash tables
- `thinc` - Machine learning library
- `wasabi` - Logging utilities
- `srsly` - Serialization utilities
- `catalogue` - Function registry
- `typer-slim` - CLI framework
- `pydantic` - Data validation
- `requests` - HTTP library
- `tqdm` - Progress bars

#### Flask Dependencies:
- `blinker` - Signal support
- `click` - CLI utilities
- `itsdangerous` - Security utilities
- `jinja2` - Template engine
- `markupsafe` - String handling
- `werkzeug` - WSGI utilities

## Installation Instructions

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Upgrade pip first
pip install --upgrade pip setuptools wheel

# Install all dependencies
pip install -r requirements_win.txt

# Install spaCy English model
python -m spacy download en_core_web_sm
```

### 3. Optional: Install Tesseract (Fallback OCR)
- **Windows**: Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
- **Linux**: `sudo apt install tesseract-ocr`
- **macOS**: `brew install tesseract`

Verify installation:
```bash
tesseract --version
```

## Jupyter Notebook Dependencies

For running the assignment notebook:
```bash
pip install jupyter matplotlib
```

## Hardware Recommendations

### Minimum Requirements:
- **CPU**: Dual-core processor
- **RAM**: 4GB
- **Storage**: 5GB free space

### Recommended for Better Performance:
- **CPU**: Quad-core processor or better
- **RAM**: 8GB or more
- **GPU**: CUDA-compatible GPU (optional, for faster EasyOCR processing)
- **Storage**: SSD for faster model loading

## GPU Support (Optional)

For faster OCR processing with GPU acceleration:

1. Install CUDA toolkit (11.0 or higher)
2. Install PyTorch with CUDA support:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```
3. Set `gpu=True` in EasyOCR initialization

## Troubleshooting

### Common Issues:

1. **EasyOCR Model Download Fails**:
   - Ensure stable internet connection
   - Models are downloaded automatically on first use (~100MB)

2. **spaCy Model Not Found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Tesseract Not Found**:
   - Install Tesseract separately
   - Add to system PATH
   - Pipeline works without Tesseract (EasyOCR only)

4. **Memory Issues**:
   - Reduce image size before processing
   - Process images one at a time
   - Close other applications

5. **Import Errors**:
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements_win.txt --force-reinstall`

## Version Compatibility

- **Python 3.8+**: Required for all dependencies
- **OpenCV 4.x**: Image processing compatibility
- **PyTorch 1.x+**: Deep learning models
- **spaCy 3.x**: NLP processing
- **Flask 2.x+**: Web framework

## Development Dependencies (Optional)

For development and testing:
```bash
pip install pytest black flake8 jupyter
```

## File Structure

```
ocr-pii-pipeline-main/
├── requirements_win.txt          # Main dependencies
├── DEPENDENCIES.md               # This file
├── OCR_PII_Pipeline_Assignment.ipynb  # Assignment notebook
├── ocr_pipeline/                 # Main package
│   ├── __init__.py
│   ├── cli.py                   # Command line interface
│   ├── api.py                   # Web API
│   ├── ocr_engine.py            # OCR processing
│   ├── preprocess.py            # Image preprocessing
│   ├── pii_detector.py          # PII detection
│   ├── text_cleaning.py         # Text cleaning
│   └── redactor.py              # Image redaction
├── samples/                      # Sample images
├── tests/                        # Unit tests
└── venv/                        # Virtual environment
```

## License Information

This pipeline uses several open-source libraries:
- **EasyOCR**: Apache 2.0 License
- **Tesseract**: Apache 2.0 License
- **spaCy**: MIT License
- **OpenCV**: Apache 2.0 License
- **Flask**: BSD License
- **PyTorch**: BSD License

Ensure compliance with respective licenses for production use.