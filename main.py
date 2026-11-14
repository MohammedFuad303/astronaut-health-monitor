import numpy as np
import pandas as pd

np.random.seed(42)
days = 90
dates = pd.date_range("2026-01-01", periods=days)

# Sleep slowly gets worse (isolation effect), HR slowly creeps up
sleep = 7.5 - np.linspace(0, 1.5, days) + np.random.normal(0, 0.4, days)
heart_rate = 60 + np.linspace(0, 8, days) + np.random.normal(0, 2, days)
mood = 8 - np.linspace(0, 2.5, days) + np.random.normal(0, 0.7, days)

df = pd.DataFrame({
    "date": dates,
    "sleep_hours": sleep.round(1),
    "resting_hr": heart_rate.round(0),
    "mood_score": mood.clip(1, 10).round(1),
})

df.to_csv("health_data.csv", index=False)
print(df.head())