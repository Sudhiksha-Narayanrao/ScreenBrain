import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image
import numpy as np
from pathlib import Path
from datetime import datetime
from utils import clean_text

def ingest_screenshot(image_path: str) -> dict:
    path = Path(image_path)
    img = Image.open(path)
    raw_text = pytesseract.image_to_string(img)
    cleaned = clean_text(raw_text)
    img_array = np.array(img)
    avg_brightness = float(np.mean(img_array))

    return {
        "filename": path.name,
        "filepath": str(path.resolve()),
        "text": cleaned,
        "word_count": len(cleaned.split()),
        "width": img.size[0],
        "height": img.size[1],
        "avg_brightness": round(avg_brightness, 2),
        "ingested_at": datetime.now().isoformat(),
    }