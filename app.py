import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Astronaut Health Monitor")

df = pd.read_csv("health_data.csv", parse_dates=["date"])

BASELINE_DAYS = 14
RECENT_DAYS = 7

baseline = df.head(BASELINE_DAYS)
recent = df.tail(RECENT_DAYS)

rows = []
for column in ["sleep_hours", "resting_hr", "mood_score"]:
    base_mean = baseline[column].mean()
    base_std = baseline[column].std()
    recent_mean = recent[column].mean()
    deviation = (recent_mean - base_mean) / base_std
    rows.append({
        "indicator": column,
        "baseline": round(base_mean, 1),
        "recent": round(recent_mean, 1),
        "deviation_sd": round(deviation, 1),
    })

DIRECTION = {"sleep_hours": -1, "resting_hr": 1, "mood_score": -1}
LABELS = {"sleep_hours": "Sleep", "resting_hr": "Heart rate", "mood_score": "Mood"}

st.subheader("Current status")
cols = st.columns(3)
for col, row in zip(cols, rows):
    name = row["indicator"]
    concern = row["deviation_sd"] * DIRECTION[name]
    text = f'{LABELS[name]}: {row["recent"]} (baseline {row["baseline"]})'
    if concern >= 2:
        col.error("🔴 " + text)
    elif concern >= 1:
        col.warning("🟡 " + text)
    else:
        col.success("🟢 " + text)

st.subheader("Change from personal baseline")
st.table(pd.DataFrame(rows))

for column in ["sleep_hours", "resting_hr", "mood_score"]:
    fig = px.line(df, x="date", y=column, title=column.replace("_", " ").title())
    st.plotly_chart(fig, use_container_width=True)