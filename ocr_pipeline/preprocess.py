# ocr_pipeline/preprocess.py
import cv2
import numpy as np

def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {path}")
    return img

def to_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def denoise(img_gray, ksize=3):
    # median filter reduces salt-and-pepper noise
    return cv2.medianBlur(img_gray, ksize)

def adaptive_thresh(img_gray, block_size=15, c=11):
    return cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, block_size, c
    )

def deskew(img_gray):
    # compute angle of rotation from non-white pixels
    coords = np.column_stack(np.where(img_gray < 255))
    if coords.size == 0:
        return img_gray
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = img_gray.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img_gray, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def morph_clean(img_bin, kernel_size=(1,1)):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    return cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)

def enhance_for_ocr(img_path, save_path=None):
    """
    Full preprocess pipeline:
      - load
      - grayscale
      - denoise
      - deskew
      - adaptive thresholding
      - optional morphological clean
    Returns: processed binary image (numpy array) and optionally saves to save_path
    """
    img = load_image(img_path)
    gray = to_grayscale(img)
    den = denoise(gray)
    desk = deskew(den)
    th = adaptive_thresh(desk)
    clean = morph_clean(th, kernel_size=(1,1))
    if save_path:
        cv2.imwrite(save_path, clean)
    return clean
