from sentence_transformers import SentenceTransformer
import chromadb
from pathlib import Path

# Load the model (downloads once, cached after)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up ChromaDB — stores everything locally in your data/ folder
client = chromadb.PersistentClient(path="data/chroma")
collection = client.get_or_create_collection(name="screenshots")


def embed_all_screenshots():
    """Read all screenshots from CSV and store their embeddings in ChromaDB."""
    import pandas as pd
    df = pd.read_csv("data/screenshots.csv")

    for _, row in df.iterrows():
        # Skip if already embedded
        existing = collection.get(ids=[row["filename"]])
        if existing["ids"]:
            print(f"Skipping (already embedded): {row['filename']}")
            continue

        # Create embedding from the extracted text
        embedding = model.encode(row["text"]).tolist()

        # Store in ChromaDB with metadata
        collection.add(
            ids=[row["filename"]],
            embeddings=[embedding],
            documents=[row["text"]],
            metadatas=[{
                "filename": row["filename"],
                "filepath": row["filepath"],
                "word_count": int(row["word_count"])
            }]
        )
        print(f"Embedded: {row['filename']}")


def search_screenshots(query: str, n_results: int = 3):
    """Search screenshots using natural language query."""
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results