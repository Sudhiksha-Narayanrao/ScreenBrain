import re

def clean_text(text: str) -> str:
    # Fix common OCR misreads
    
    text = re.sub(r'[^\x20-\x7E\n₹]', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    # Fix common OCR misread: % followed by digits is likely ₹
    text = re.sub(r'%(\d)', r'₹\1', text)
    return text.strip()

def is_image_file(path: str) -> bool:
    return path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))