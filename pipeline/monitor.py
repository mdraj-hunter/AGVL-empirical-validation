import sqlite3
from datetime import datetime

DB_PATH = 'monitoring.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            stage TEXT,
            question_id TEXT,
            question TEXT,
            model_answer TEXT,
            gold_answer TEXT,
            judge_verdict TEXT,
            confidence TEXT,
            needs_review TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_run(stage, question_id, question, model_answer, gold_answer,
            judge_verdict='', confidence='', needs_review=''):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        INSERT INTO pipeline_runs
        (timestamp, stage, question_id, question, model_answer, gold_answer, judge_verdict, confidence, needs_review)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), stage, question_id, question, model_answer,
          gold_answer, judge_verdict, confidence, needs_review))
    conn.commit()
    conn.close()

init_db()