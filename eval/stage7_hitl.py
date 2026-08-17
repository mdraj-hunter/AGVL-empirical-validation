import csv

with open('results/stage6_consensus_results.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

flagged = []
passed = []

for r in rows:
    needs_review = (r['consensus_status'] == 'DISAGREE') or (r['confidence'] == 'LOW')
    r['needs_review'] = 'YES' if needs_review else 'NO'
    if needs_review:
        flagged.append(r)
    else:
        passed.append(r)

with open('results/stage7_review_queue.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Total: {len(rows)}")
print(f"Routed to human review: {len(flagged)} ({100*len(flagged)/len(rows):.1f}%)")
print(f"Passed automatically: {len(passed)} ({100*len(passed)/len(rows):.1f}%)")