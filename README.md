# ScreenBrain 
> A RAG-powered app that turns your screenshots into a searchable AI second brain.

## What it does

You take screenshots every day — articles, code snippets, prices, notes — and they sit in a folder, never to be found again. ScreenBrain fixes that.

Drop your screenshots into a folder and ScreenBrain will:
- **Read** all text inside them using OCR
- **Understand** the meaning of each screenshot using BERT embeddings
- **Answer** your natural language questions about them using LLaMA 3.3
- **Show** you the exact screenshot the answer came from

## Demo

> Type: *"what algorithm searches in a sorted matrix?"*
> 
> ScreenBrain finds the right screenshot and answers: *"The algorithm starts from the top-right corner, moving left if the target is smaller and down if the target is larger, achieving O(m+n) time complexity."*

## Tech Stack

| Layer | Technology |
|-------|-----------|
| OCR | Tesseract + pytesseract |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2 / BERT) |
| Vector Database | ChromaDB |
| LLM | LLaMA 3.3 70B via Groq API |
| UI | Streamlit |
| Data | pandas, numpy |

## Architecture

```
screenshot.png
    │
    ▼
Tesseract OCR ──► extracted text
    │
    ▼
sentence-transformers ──► 384-dimensional embedding
    │
    ▼
ChromaDB ──► stored vector + metadata
    │
    ▼
User query ──► embed query ──► similarity search
    │
    ▼
Top-k screenshots retrieved ──► LLaMA 3.3 via Groq
    │
    ▼
Grounded answer + source screenshot displayed
```

## Project Structure

```
screenbrain/
├── screenshots/        # Drop your screenshots here
├── data/
│   ├── screenshots.csv # Extracted text + metadata
│   └── chroma/         # Vector database
├── ingest.py           # OCR + image analysis pipeline
├── store.py            # CSV database operations
├── embedder.py         # Embedding + ChromaDB search
├── ask.py              # CLI interface for RAG queries
├── app.py              # Streamlit web interface
├── run.py              # Batch ingest runner
├── utils.py            # Text cleaning helpers
└── requirements.txt
```

## Setup

### Prerequisites
- Python 3.10+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your OS

### Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at [console.groq.com](https://console.groq.com)

### Run

**Step 1 — Add screenshots**
```bash
# Drop your .png / .jpg screenshots into the screenshots/ folder
python run.py   # ingest and embed all screenshots
```

**Step 2 — Launch the app**
```bash
streamlit run app.py
```

**Step 3 — Search**

Open `http://localhost:8501` and type any natural language question about your screenshots.

## How RAG Works Here

Without RAG, an LLM answers from training data alone — it might hallucinate or not know your specific content.

With RAG:
1. Your question is converted to an embedding
2. ChromaDB finds the most semantically similar screenshots
3. The actual screenshot text is passed to LLaMA as context
4. LLaMA answers *only* from your screenshots — grounded, not hallucinated

## Known Limitations

- OCR may misread special characters (e.g. ₹ may appear as %)
- Screenshots with very little text (< 10 words) may not retrieve well
- Free Groq API tier has rate limits — wait 60 seconds between heavy usage

## Roadmap

- [ ] K-Means topic clustering (scikit-learn)
- [ ] Auto keyword tagging (TF-IDF)
- [ ] Visual screenshot classification (TensorFlow / MobileNetV2)
- [ ] Hallucination comparison demo
- [ ] FastAPI backend
- [ ] Deployment on Railway / Render

## Built By

[Sudhiksha Narayanrao](https://github.com/Sudhiksha-Narayanrao) — B.Tech CS, Mahindra University
