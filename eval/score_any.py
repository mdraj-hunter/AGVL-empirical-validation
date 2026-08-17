import csv
import re
import ollama
import sys

def score_file(input_path, output_path, label):
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    results = []
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

        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[{'role': 'user', 'content': judge_prompt}],
            options={'temperature': 0}
        )
        raw = response['message']['content']

        match = re.search(r'FINAL_VERDICT:\s*(CORRECT|HALLUCINATED)', raw, re.IGNORECASE)
        verdict = match.group(1).upper() if match else 'UNPARSEABLE'

        row['judge_verdict'] = verdict
        row['judge_raw'] = raw
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

    print(f"\n=== {label} ===")
    print(f"Total: {total} | Correct: {correct} | Hallucinated: {hallucinated} | Unparseable: {unparseable}")
    if (correct + hallucinated) > 0:
        rate = 100 * hallucinated / (correct + hallucinated)
        print(f"Hallucination rate (of parseable): {rate:.1f}%")


if __name__ == '__main__':
    input_file = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else input_file
    output_file = f"results/{input_file.replace('_results.csv', '')}_scored.csv"
    score_file(f"results/{input_file}", output_file, label)