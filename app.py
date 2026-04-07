import streamlit as st
from embedder import embed_all_screenshots, search_screenshots
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="ScreenBrain", page_icon="🧠")
st.title("🧠 ScreenBrain")
st.caption("Search your screenshots using natural language")

with st.sidebar:
    st.header("Add Screenshots")
    if st.button("Sync screenshots"):
        with st.spinner("Reading and embedding..."):
            embed_all_screenshots()
        st.success("Done!")

query = st.text_input("Ask anything about your screenshots...")

if query:
    with st.spinner("Searching..."):
        results = search_screenshots(query, n_results=3)
        context = ""
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context += f"\nScreenshot: {meta['filename']}\nContent: {doc}\n"

        prompt = f"""You are ScreenBrain, an AI that answers questions based on 
the user's saved screenshots.

Here are the relevant screenshots found:
{context}

User question: {query}

Answer based only on the screenshot content above. Be concise.
Do not convert or change any currency symbols — use exactly what appears in the screenshots."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content

    st.markdown("### Answer")
    st.write(answer)

    st.markdown("### Sources")
    top_meta = results["metadatas"][0][0]
    st.caption(f"Source: {top_meta['filename']}")
    try:
        st.image(top_meta["filepath"], width=300)
    except:
        st.caption("(image could not be displayed)")