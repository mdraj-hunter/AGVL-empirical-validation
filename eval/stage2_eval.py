import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import ollama
import csv
import time
from pipeline.stage2_rag import retrieve_context

with open('data/subset_150.json', 'r', encoding='utf-8') as f:
    subset = json.load(f)

results = []

for i, item in enumerate(subset):
    question = item['question']
    gold_answer = item['right_answer']

    retrieved = retrieve_context(question, k=3)
    context_block = "\n".join(f"- {passage}" for passage in retrieved)

    prompt = f"""Use the following retrieved context to answer the question. If the context doesn't contain the answer, say so rather than guessing.

Context:
{context_block}

Question: {question}
Answer in one short sentence. State only the factual answer, no explanation:"""

    start = time.time()
    response = ollama.chat(model='llama3.2:3b', messages=[{'role': 'user', 'content': prompt}])
    elapsed = time.time() - start

    results.append({
        'id': i,
        'question': question,
        'gold_answer': gold_answer,
        'model_answer': response['message']['content'],
        'elapsed_sec': round(elapsed, 1)
    })
    print(f"[{i+1}/{len(subset)}] ({elapsed:.1f}s) {question[:60]}...")

with open('results/stage2_rag_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Stage 2 (RAG) run complete.")