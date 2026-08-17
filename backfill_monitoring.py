import csv
import sqlite3
from pipeline.monitor import log_run, init_db, DB_PATH

init_db()

# Clear existing data so re-running doesn't duplicate rows
conn = sqlite3.connect(DB_PATH)
conn.execute("DELETE FROM pipeline_runs")
conn.commit()
conn.close()

stages = [
    ('baseline', 'results/baseline_scored_v2.csv'),
    ('rag', 'results/stage2_scored_v2.csv'),       # fixed: was stage2_scored.csv
    ('cot', 'results/stage3_cot_scored.csv'),
    ('uncertainty', 'results/stage4_uncertainty_scored.csv'),
    ('critic', 'results/stage5_critic_scored.csv'),
    ('consensus_hitl', 'results/stage7_review_queue.csv'),  # new: brings in needs_review data
]

for stage_name, path in stages:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            log_run(
                stage=stage_name,
                question_id=r.get('id', ''),
                question=r.get('question', ''),
                model_answer=r.get('model_answer', ''),
                gold_answer=r.get('gold_answer', ''),
                judge_verdict=r.get('judge_verdict', ''),
                confidence=r.get('confidence', ''),
                needs_review=r.get('needs_review', '')
            )
        print(f"Backfilled {len(rows)} rows for stage: {stage_name}")
    except FileNotFoundError:
        print(f"Skipped {stage_name}, file not found: {path}")

print("Backfill complete.")