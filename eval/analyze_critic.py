import csv

with open('results/stage5_critic_scored.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

kept = [r for r in rows if r['critic_action'] == 'KEPT']
revised = [r for r in rows if r['critic_action'] == 'REVISED']

def hallucination_rate(subset):
    correct = sum(1 for r in subset if r['judge_verdict'] == 'CORRECT')
    hallucinated = sum(1 for r in subset if r['judge_verdict'] == 'HALLUCINATED')
    total = correct + hallucinated
    return (100 * hallucinated / total) if total else 0, total

kept_rate, kept_total = hallucination_rate(kept)
revised_rate, revised_total = hallucination_rate(revised)

print(f"KEPT (critic agreed):    {kept_total} questions, {kept_rate:.1f}% hallucination rate")
print(f"REVISED (critic changed): {revised_total} questions, {revised_rate:.1f}% hallucination rate")