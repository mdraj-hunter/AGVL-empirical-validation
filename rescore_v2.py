import csv
import ollama
import re

def score_file(input_path, output_path, label):
    results = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for i, row in enumerate(rows):
        judge_prompt = f"""You are grading whether a model's answer is factually correct.

Question: {row['question']}
Gold (correct) answer: {row['gold_answer']}
Model's answer: {row['model_answer']}

Does the model's answer convey the same factual content as the gold answer, even if worded differently?
You may briefly explain your reasoning, but you MUST end your response with exactly this format on its own line:
FINAL_VERDICT: CORRECT
or
FINAL_VERDICT: HALLUCINATED"""

        response = ollama.chat(model='qwen2.5:3b', messages=[
            {'role': 'user', 'content': judge_prompt}
        ])
        raw = response['message']['content']

        match = re.search(r'FINAL_VERDICT:\s*(CORRECT|HALLUCINATED)', raw, re.IGNORECASE)
        verdict = match.group(1).upper() if match else 'UNPARSEABLE'

        row['judge_verdict'] = verdict
        row['judge_raw'] = raw  # keep for auditing
        results.append(row)

        print(f"[{i+1}/{len(rows)}] {verdict}")

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    correct = sum(1 for r in results if r['judge_verdict'] == 'CORRECT')
    hallucinated = sum(1 for r in results if r['judge_verdict'] == 'HALLUCINATED')
    unparseable = sum(1 for r in results if r['judge_verdict'] == 'UNPARSEABLE')
    total = len(results)

    print(f"\n=== {label} RESULTS ===")
    print(f"Correct: {correct}/{total}")
    print(f"Hallucinated: {hallucinated}/{total}")
    print(f"Unparseable (needs manual check): {unparseable}/{total}")
    print(f"Hallucination rate (of parseable): {100*hallucinated/(correct+hallucinated):.1f}%")

score_file('results/baseline_results.csv', 'results/baseline_scored_v2.csv', 'BASELINE')
score_file('results/stage2_rag_results.csv', 'results/stage2_scored_v2.csv', 'STAGE 2 (RAG)')