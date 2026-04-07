import os
from dotenv import load_dotenv
from groq import Groq
from embedder import search_screenshots

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_screenbrain(query: str):
    results = search_screenshots(query, n_results=2)
    
    context = ""
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context += f"\nScreenshot: {meta['filename']}\nContent: {doc}\n"
    
    prompt = f"""You are ScreenBrain, an AI that answers questions based on 
the user's saved screenshots.

Here are the relevant screenshots found:
{context}

User question: {query}

Answer based only on the screenshot content above. Be concise."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(f"\nQuestion: {query}")
    print(f"\nAnswer: {response.choices[0].message.content}")
    print(f"\nSources: {[m['filename'] for m in results['metadatas'][0]]}")

ask_screenbrain("what algorithm searches in a sorted matrix?")