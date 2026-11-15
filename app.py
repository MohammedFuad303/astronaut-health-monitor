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


st.subheader("Daily check-in")
with st.form("checkin"):
    sleep_in = st.number_input("Sleep last night (hours)", 0.0, 14.0, 7.0, 0.1)
    hr_in = st.number_input("Resting heart rate (bpm)", 30, 150, 60)
    mood_in = st.slider("Mood today (1-10)", 1, 10, 7)
    submitted = st.form_submit_button("Save check-in")


if submitted:
    new_row = pd.DataFrame([{
        "date": df["date"].max() + pd.Timedelta(days=1),
        "sleep_hours": sleep_in,
        "resting_hr": hr_in,
        "mood_score": mood_in,
    }])
    new_row.to_csv("health_data.csv", mode="a", header=False, index=False)
    st.rerun()


ADVICE = {
    "sleep_hours": {
        "yellow": "Sleep is trending down. Keep a fixed sleep schedule and dim lights before bed.",
        "red": "Sleep is well below baseline. Report to the flight surgeon and review the sleep schedule.",
    },
    "resting_hr": {
        "yellow": "Resting heart rate is rising. Review exercise load and hydration.",
        "red": "Resting heart rate is well above baseline. Schedule a cardiovascular check with the flight surgeon.",
    },
    "mood_score": {
        "yellow": "Mood is declining. Schedule a private call with family or a friend.",
        "red": "Mood is well below baseline. Contact the behavioral health team.",
    },
}

st.subheader("Recommended actions")
any_alert = False
for row in rows:
    name = row["indicator"]
    concern = row["deviation_sd"] * DIRECTION[name]
    if concern >= 2:
        st.error("🔴 " + ADVICE[name]["red"])
        any_alert = True
    elif concern >= 1:
        st.warning("🟡 " + ADVICE[name]["yellow"])
        any_alert = True
if not any_alert:
    st.success("🟢 All indicators are within normal range. Keep up the routine.")

st.caption("Prototype for the NASA Space Apps Challenge. Not medical advice.")