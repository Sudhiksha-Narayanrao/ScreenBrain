from embedder import embed_all_screenshots, search_screenshots

# Step 1 — embed all screenshots
print("Embedding screenshots...")
embed_all_screenshots()

# Step 2 — search!
print("\n--- Search Results ---")
query = "algorithm to search in a matrix"
results = search_screenshots(query)

for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
    print(f"\nResult {i+1}: {meta['filename']}")
    print(f"Preview: {doc[:150]}...")