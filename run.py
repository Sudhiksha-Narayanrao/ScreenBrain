from ingest import ingest_screenshot
from store import save_record, show_summary
from pathlib import Path
from utils import is_image_file

SCREENSHOTS_DIR = Path("screenshots")

for img_path in SCREENSHOTS_DIR.iterdir():
    if is_image_file(img_path.name):
        record = ingest_screenshot(img_path)
        save_record(record)

show_summary()