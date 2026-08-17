import csv
import ollama
import time

results = []
with open('results/stage2_rag_results.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for i, row in enumerate(rows):
    judge_prompt = f"""You are grading whether a model's answer is factually correct.

Question: {row['question']}
Gold (correct) answer: {row['gold_answer']}
Model's answer: {row['model_answer']}

Does the model's answer convey the same factual content as the gold answer, even if worded differently?
Respond with ONLY a single word on its own line, nothing else before or after: CORRECT or HALLUCINATED"""

    response = ollama.chat(model='qwen2.5:3b', messages=[
        {'role': 'user', 'content': judge_prompt}
    ])

    verdict_raw = response['message']['content'].strip().upper()
    first_word = verdict_raw.split()[0].strip('.,!:') if verdict_raw else ''
    verdict = 'CORRECT' if first_word == 'CORRECT' else 'HALLUCINATED'

    row['judge_verdict'] = verdict
    results.append(row)

    print(f"[{i+1}/{len(rows)}] {verdict}")

with open('results/stage2_scored.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

correct = sum(1 for r in results if r['judge_verdict'] == 'CORRECT')
total = len(results)
hallucination_rate = 100 * (total - correct) / total

print(f"\n=== STAGE 2 (RAG) RESULTS ===")
print(f"Correct: {correct}/{total}")
print(f"Hallucination rate: {hallucination_rate:.1f}%")