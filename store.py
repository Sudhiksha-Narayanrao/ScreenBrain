import pandas as pd
from pathlib import Path

DB_PATH = Path("data/screenshots.csv")

def load_db() -> pd.DataFrame:
    if DB_PATH.exists():
        return pd.read_csv(DB_PATH)
    return pd.DataFrame(columns=[
        "filename", "filepath", "text", "word_count",
        "width", "height", "avg_brightness", "ingested_at"
    ])

def save_record(record: dict):
    df = load_db()
    if record["filename"] in df["filename"].values:
        print(f"Skipping duplicate: {record['filename']}")
        return
    new_row = pd.DataFrame([record])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_PATH, index=False)
    print(f"Saved: {record['filename']} ({record['word_count']} words)")

def show_summary():
    df = load_db()
    print(f"\n=== ScreenBrain Store ===")
    print(f"Total screenshots : {len(df)}")
    print(f"Total words       : {df['word_count'].sum()}")
    print(f"Avg words/screen  : {df['word_count'].mean():.1f}")
    print(df[["filename", "word_count", "ingested_at"]].to_string(index=False))