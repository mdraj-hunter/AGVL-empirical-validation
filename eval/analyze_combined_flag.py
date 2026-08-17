import csv

with open('results/stage6_consensus_results.csv', 'r', encoding='utf-8') as f:
    consensus_rows = {r['id']: r for r in csv.DictReader(f)}

with open('results/stage4_uncertainty_scored.csv', 'r', encoding='utf-8') as f:
    scored_rows = list(csv.DictReader(f))

flagged_verdicts = []
unflagged_verdicts = []

for r in scored_rows:
    c = consensus_rows.get(r['id'])
    if not c:
        continue
    is_flagged = (c['consensus_status'] == 'DISAGREE') or (c['confidence'] == 'LOW')
    if is_flagged:
        flagged_verdicts.append(r['judge_verdict'])
    else:
        unflagged_verdicts.append(r['judge_verdict'])

def rate(verdicts):
    correct = verdicts.count('CORRECT')
    hallucinated = verdicts.count('HALLUCINATED')
    total = correct + hallucinated
    return (100 * hallucinated / total) if total else 0, total

f_rate, f_total = rate(flagged_verdicts)
u_rate, u_total = rate(unflagged_verdicts)

print(f"FLAGGED (either signal):   {f_total} questions, {f_rate:.1f}% hallucination rate")
print(f"UNFLAGGED (neither):       {u_total} questions, {u_rate:.1f}% hallucination rate")