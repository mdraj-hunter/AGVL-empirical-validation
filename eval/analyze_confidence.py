import csv

with open('results/stage4_uncertainty_scored.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

high_conf = [r for r in rows if r['confidence'] == 'HIGH']
low_conf = [r for r in rows if r['confidence'] == 'LOW']

def hallucination_rate(subset):
    correct = sum(1 for r in subset if r['judge_verdict'] == 'CORRECT')
    hallucinated = sum(1 for r in subset if r['judge_verdict'] == 'HALLUCINATED')
    total = correct + hallucinated
    return (100 * hallucinated / total) if total else 0, total

high_rate, high_total = hallucination_rate(high_conf)
low_rate, low_total = hallucination_rate(low_conf)

print(f"HIGH confidence: {high_total} questions, {high_rate:.1f}% hallucination rate")
print(f"LOW confidence:  {low_total} questions, {low_rate:.1f}% hallucination rate")