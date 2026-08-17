import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import ollama
import csv
import time
from collections import Counter
from pipeline.stage2_rag import retrieve_context

with open('data/subset_150.json', 'r', encoding='utf-8') as f:
    subset = json.load(f)

def get_sample(prompt):
    response = ollama.chat(
        model='llama3.2:3b',
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0.7}
    )
    return response['message']['content']

results = []

for i, item in enumerate(subset):
    question = item['question']
    gold_answer = item['right_answer']

    retrieved = retrieve_context(question, k=3)
    context_block = "\n".join(f"- {passage}" for passage in retrieved)

    prompt = f"""Use the following retrieved context to answer the question.

Context:
{context_block}

Question: {question}
Answer in one short sentence. State only the factual answer, no explanation:"""

    start = time.time()
    samples = [get_sample(prompt) for _ in range(3)]
    elapsed = time.time() - start

    # Normalize for comparison (lowercase, strip) without destroying original text
    normalized = [s.strip().lower() for s in samples]
    counts = Counter(normalized)
    most_common_norm, agreement_count = counts.most_common(1)[0]

    # Find the original-cased sample matching the most common normalized answer
    final_answer = next(s for s, n in zip(samples, normalized) if n == most_common_norm)
    confidence = 'HIGH' if agreement_count >= 2 else 'LOW'

    results.append({
        'id': i,
        'question': question,
        'gold_answer': gold_answer,
        'model_answer': final_answer,
        'sample_1': samples[0],
        'sample_2': samples[1],
        'sample_3': samples[2],
        'agreement_count': agreement_count,
        'confidence': confidence,
        'elapsed_sec': round(elapsed, 1)
    })
    print(f"[{i+1}/{len(subset)}] ({elapsed:.1f}s) confidence={confidence} {question[:50]}...")

with open('results/stage4_uncertainty_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Stage 4 (Uncertainty Quantification) run complete.")