from PIL import Image
import pytesseract
import tempfile
import cv2
import numpy as np

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    scale_percent = 150
    width = int(thresh.shape[1] * scale_percent / 100)
    height = int(thresh.shape[0] * scale_percent / 100)
    resized = cv2.resize(thresh, (width, height), interpolation=cv2.INTER_LINEAR)
    return resized

def extract_text_from_image(content: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(content)
        tmp.close()

        processed = preprocess_image(tmp.name)
        preprocessed_path = tmp.name + "_processed.png"
        cv2.imwrite(preprocessed_path, processed)

        text = pytesseract.image_to_string(Image.open(preprocessed_path))

        return text