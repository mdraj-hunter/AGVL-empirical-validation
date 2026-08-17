import csv

def summarize(path, label):
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    correct = sum(1 for r in rows if r['judge_verdict'] == 'CORRECT')
    hallucinated = sum(1 for r in rows if r['judge_verdict'] == 'HALLUCINATED')
    unparseable = sum(1 for r in rows if r['judge_verdict'] == 'UNPARSEABLE')
    total = len(rows)

    print(f"\n=== {label} ===")
    print(f"Total: {total}")
    print(f"Correct: {correct}")
    print(f"Hallucinated: {hallucinated}")
    print(f"Unparseable: {unparseable}")
    if (correct + hallucinated) > 0:
        rate = 100 * hallucinated / (correct + hallucinated)
        print(f"Hallucination rate (of parseable): {rate:.1f}%")

summarize('results/baseline_scored_v2.csv', 'BASELINE')
summarize('results/stage2_scored_v2.csv', 'STAGE 2 (RAG)')