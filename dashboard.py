import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="AGVL Pipeline Monitor", layout="wide")
st.title("AGVL — Production Monitoring Dashboard")

conn = sqlite3.connect('monitoring.db')
df = pd.read_sql_query("SELECT * FROM pipeline_runs", conn)
conn.close()

if df.empty:
    st.warning("No data yet — run backfill_monitoring.py first.")
else:
    st.subheader("Hallucination Rate by Stage")
    stage_stats = df[df['judge_verdict'] != ''].groupby('stage')['judge_verdict'].apply(
        lambda x: 100 * (x == 'HALLUCINATED').sum() / len(x)
    ).reset_index()
    stage_stats.columns = ['Stage', 'Hallucination Rate (%)']
    st.bar_chart(stage_stats.set_index('Stage'))

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Logged Runs", len(df))
    col2.metric("Stages Tracked", df['stage'].nunique())
    flagged = (df['needs_review'] == 'YES').sum()
    col3.metric("Flagged for Review", flagged)

    st.subheader("Raw Run Log")
    st.dataframe(df, use_container_width=True)