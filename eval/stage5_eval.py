import csv
import ollama
import time

with open('results/stage4_uncertainty_results.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

results = []

for i, row in enumerate(rows):
    question = row['question']
    gold_answer = row['gold_answer']
    original_answer = row['model_answer']
    confidence = row['confidence']

    critic_prompt = f"""You are a fact-checking critic reviewing another AI's answer.

Question: {question}
Proposed answer: {original_answer}

Review this answer for factual errors. If it is correct, respond with:
VERDICT: KEEP

If it contains an error, respond with:
VERDICT: REVISE
CORRECTED_ANSWER: <your corrected one-sentence answer>"""

    start = time.time()
    response = ollama.chat(
        model='qwen2.5:3b',
        messages=[{'role': 'user', 'content': critic_prompt}],
        options={'temperature': 0}
    )
    elapsed = time.time() - start

    raw = response['message']['content']

    if 'VERDICT: REVISE' in raw.upper() and 'CORRECTED_ANSWER:' in raw.upper():
        # Extract text after CORRECTED_ANSWER:
        idx = raw.upper().find('CORRECTED_ANSWER:')
        final_answer = raw[idx + len('CORRECTED_ANSWER:'):].strip()
        critic_action = 'REVISED'
    else:
        final_answer = original_answer
        critic_action = 'KEPT'

    results.append({
        'id': row['id'],
        'question': question,
        'gold_answer': gold_answer,
        'model_answer': final_answer,
        'original_answer': original_answer,
        'confidence': confidence,
        'critic_action': critic_action,
        'critic_raw': raw,
        'elapsed_sec': round(elapsed, 1)
    })
    print(f"[{i+1}/{len(rows)}] ({elapsed:.1f}s) critic={critic_action} confidence={confidence}")

with open('results/stage5_critic_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Stage 5 (Critic Model) run complete.")