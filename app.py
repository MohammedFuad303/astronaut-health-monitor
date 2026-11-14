import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Astronaut Health Monitor")

df = pd.read_csv("health_data.csv", parse_dates=["date"])

for column in ["sleep_hours", "resting_hr", "mood_score"]:
    fig = px.line(df, x="date", y=column, title=column.replace("_", " ").title())
    st.plotly_chart(fig, use_container_width=True)