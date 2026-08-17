import json
import ollama
import csv
import time

with open('data/subset_150.json', 'r', encoding='utf-8') as f:
    subset = json.load(f)

results = []

for i, item in enumerate(subset):
    question = item['question']
    gold_answer = item['right_answer']

    prompt = f"Answer the following question in one short sentence. State only the factual answer, no explanation:\n\n{question}"

    start = time.time()
    response = ollama.chat(model='llama3.2:3b', messages=[
        {'role': 'user', 'content': prompt}
    ])
    elapsed = time.time() - start

    model_answer = response['message']['content']

    results.append({
        'id': i,
        'question': question,
        'gold_answer': gold_answer,
        'model_answer': model_answer,
        'elapsed_sec': round(elapsed, 1)
    })

    print(f"[{i+1}/{len(subset)}] ({elapsed:.1f}s) {question[:60]}...")

with open('results/baseline_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Baseline run complete. Saved to results/baseline_results.csv")