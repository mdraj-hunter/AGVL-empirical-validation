import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import csv
import ollama
import time
from pipeline.stage2_rag import retrieve_context

with open('results/stage4_uncertainty_results.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

def ask_model(model_name, question, context_block):
    prompt = f"""Use the following retrieved context to answer the question.

Context:
{context_block}

Question: {question}
Answer in one short sentence. State only the factual answer, no explanation:"""

    response = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0}
    )
    return response['message']['content']

results = []

for i, row in enumerate(rows):
    question = row['question']
    gold_answer = row['gold_answer']
    llama_answer = row['model_answer']  # reuse Stage 4's Llama answer, don't regenerate

    retrieved = retrieve_context(question, k=3)
    context_block = "\n".join(f"- {passage}" for passage in retrieved)

    start = time.time()
    qwen_answer = ask_model('qwen2.5:3b', question, context_block)
    elapsed = time.time() - start

    # Simple agreement heuristic: normalized substring overlap
    llama_norm = llama_answer.strip().lower()
    qwen_norm = qwen_answer.strip().lower()
    agree = llama_norm in qwen_norm or qwen_norm in llama_norm

    consensus_status = 'AGREE' if agree else 'DISAGREE'
    # On disagreement, keep Llama's answer as the default (no tiebreaker model available)
    final_answer = llama_answer

    results.append({
        'id': row['id'],
        'question': question,
        'gold_answer': gold_answer,
        'model_answer': final_answer,
        'llama_answer': llama_answer,
        'qwen_answer': qwen_answer,
        'consensus_status': consensus_status,
        'confidence': row['confidence'],  # carried forward from Stage 4
        'elapsed_sec': round(elapsed, 1)
    })
    print(f"[{i+1}/{len(rows)}] ({elapsed:.1f}s) consensus={consensus_status}")

with open('results/stage6_consensus_results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Stage 6 (Cross-Model Consensus) run complete.")