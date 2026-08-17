import json
import chromadb
from sentence_transformers import SentenceTransformer

with open('data/qa_data.json', 'r', encoding='utf-8') as f:
    all_examples = [json.loads(line) for line in f]

unique_knowledge = list({ex['knowledge'] for ex in all_examples if ex.get('knowledge')})
print(f"Building corpus from {len(unique_knowledge)} unique knowledge passages")

embedder = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("halueval_knowledge")

if collection.count() == 0:
    embeddings = embedder.encode(unique_knowledge, show_progress_bar=True).tolist()
    ids = [str(i) for i in range(len(unique_knowledge))]

    batch_size = 5000
    for start in range(0, len(unique_knowledge), batch_size):
        end = start + batch_size
        collection.add(
            embeddings=embeddings[start:end],
            documents=unique_knowledge[start:end],
            ids=ids[start:end]
        )
        print(f"Added batch {start}-{min(end, len(unique_knowledge))}")

    print(f"Indexed {len(unique_knowledge)} passages")
else:
    print(f"Using existing index with {collection.count()} passages")


def retrieve_context(question, k=3):
    query_embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=k)
    # Safely handle cases where the query returns no documents or None
    if not results:
        return []
    docs = results.get('documents') if isinstance(results, dict) else None
    if not docs or not docs[0]:
        return []
    return docs[0]