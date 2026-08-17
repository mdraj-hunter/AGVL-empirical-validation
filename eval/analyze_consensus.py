import csv

with open('results/stage6_consensus_results.csv', 'r', encoding='utf-8') as f:
    consensus_rows = {r['id']: r['consensus_status'] for r in csv.DictReader(f)}

with open('results/stage4_uncertainty_scored.csv', 'r', encoding='utf-8') as f:
    scored_rows = list(csv.DictReader(f))

agree_verdicts = []
disagree_verdicts = []

for r in scored_rows:
    status = consensus_rows.get(r['id'])
    if status == 'AGREE':
        agree_verdicts.append(r['judge_verdict'])
    elif status == 'DISAGREE':
        disagree_verdicts.append(r['judge_verdict'])

def rate(verdicts):
    correct = verdicts.count('CORRECT')
    hallucinated = verdicts.count('HALLUCINATED')
    total = correct + hallucinated
    return (100 * hallucinated / total) if total else 0, total

agree_rate, agree_total = rate(agree_verdicts)
disagree_rate, disagree_total = rate(disagree_verdicts)

print(f"AGREE:    {agree_total} questions, {agree_rate:.1f}% hallucination rate")
print(f"DISAGREE: {disagree_total} questions, {disagree_rate:.1f}% hallucination rate")