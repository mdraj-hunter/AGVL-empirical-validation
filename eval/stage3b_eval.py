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

    prompt = f"""Use the following retrieved context to answer the question.

Context:
{context_block}

Question: {question}

Think through this step by step:
1. What is the question actually asking?
2. Which parts of the context are relevant?
3. What is the answer based on that context?

Important: your FINAL_ANSWER must be consistent with your own reasoning above. Do not contradict your own conclusion.

Show your reasoning briefly, then end your response with exactly this format on its own line:
FINAL_ANSWER: <your one-sentence answer>"""

    start = time.time()
    response = ollama.chat(
        model='llama3.2:3b',
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0}
    )
    elapsed = time.time() - start

    results.append({
        'id': i,
        'question': question,
        'gold_answer': gold_answer,
        'model_answer': response['message']['content'],
        'elapsed_sec': round(elapsed, 1)
    })
    print(f"[{i+1}/{len(subset)}] ({elapsed:.1f}s) {question[:60]}...")

with open('results/stage3b_cot_fixed_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Stage 3b (CoT, consistency-fixed) run complete.")