import csv

with open('results/stage6_consensus_results.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

both_flagged = sum(1 for r in rows if r['consensus_status'] == 'DISAGREE' and r['confidence'] == 'LOW')
only_consensus = sum(1 for r in rows if r['consensus_status'] == 'DISAGREE' and r['confidence'] == 'HIGH')
only_uncertainty = sum(1 for r in rows if r['consensus_status'] == 'AGREE' and r['confidence'] == 'LOW')
neither = sum(1 for r in rows if r['consensus_status'] == 'AGREE' and r['confidence'] == 'HIGH')

print(f"Flagged by BOTH signals:      {both_flagged}")
print(f"Flagged by consensus ONLY:    {only_consensus}")
print(f"Flagged by uncertainty ONLY:  {only_uncertainty}")
print(f"Flagged by NEITHER:           {neither}")