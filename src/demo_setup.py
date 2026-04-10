# Create Demo Dataset

import numpy as np
import pandas as pd
import random
from pathlib import Path

# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir_demo = root / 'data/demo'

player_sample = ['Player A','Player B','Player C','Player D','Player E','Player F','Player G','Player H',
                 'Player I','Player J','Player K','Player L','Player M','Player N','Player O','Player P',
                 'Player Q','Player R','Player S']

position_sample = ['Goalkeeper','Center Back','Outside Back','Center Midfielder','Outside Midfielder','Striker']
player_positions = {player: random.choice(position_sample) for player in player_sample}

dates_model = pd.date_range(start="2024-08-01",end="2024-11-30",freq="D")
dates_current = pd.date_range(start="2025-08-01",end="2025-11-30",freq="D")

#########################################################################################
# Functions for Demo Data
def gps_demo(dates_range,model):
    df = pd.DataFrame(
        [(date, player, player_positions[player]) for date in dates_range for player in player_sample],
        columns = ["Start Date","Athlete Name","Athlete Position"]
    )

    # Add session type
    df["Session Type"] = df["Start Date"].dt.dayofweek.map(
        lambda x: "Match Session" if x in (1, 5) else "Training Session"
    )

    # Get Start and End Times
    df["Start Time"] = df["Session Type"].map(
        lambda x: "12:00" if x in ("Match Session") else "16:30"
    )
    df["Start Time (s)"] = df["Session Type"].map(
        lambda x: "12:00:00" if x in ("Match Session") else "16:30:00"
    )
    df["End Time (s)"] = df["Session Type"].map(
        lambda x: "13:30:00" if x in ("Match Session") else "18:00:00"
    )

    # First day of the week (Monday)
    df["Week Start Date"] = df["Start Date"] - pd.to_timedelta(df["Start Date"].dt.dayofweek, unit="D")

    # First day of the month
    df["Month Start Date"] = df["Start Date"].dt.to_period("M").dt.to_timestamp()

    # Add Tags and Segment Name
    df["Tags"] = "None"
    df["Segment Name"] = "Whole Session"

    # Person ID
    df["Person ID"] = df["Athlete Name"]
    df["Athlete Groups"] = df["Athlete Position"]

    # Add GPS Metrics
    np.random.seed(19)
    df["Duration (minutes)"] = 90

    # Integer Metrics
    int_metrics = {
        "Session Load": (100,1200),
        "Distance (yds)": (2000,14000),
        "No. of High Intensity Events": (0,60),
        "No. of Sprints": (0,12),
        "Accelerations": (10,100),
        "Decelerations": (10,100),
        "Percentage of Max Speed": (75,100)
    }

    for col, (low, high) in int_metrics.items():
        df[col] = np.random.randint(low=low, high=high, size=len(df))

    # Float Metrics
    float_metrics = {
        "high_intensity_avg": (8.0,20.0),
        "sprint_avg": (15.0,40.0),
        "Top Speed (mph)": (14.0,20.5),
        "Avg Speed (mph)": (1.5, 7),
    }
    for col, (low, high) in float_metrics.items():
        df[col] = np.random.uniform(low=low, high=high, size=len(df)).round(1)

    # Final Metrics for Sprint yds and High intensity yards & Yard per minute
    df["High Intensity Running (yds)"] = round(df["No. of High Intensity Events"] * df["high_intensity_avg"],0)
    df["Sprint Distance (yds)"] = round(df["No. of Sprints"] * df["sprint_avg"],0)
    df["Yards per Minute (yds)"] = round(df["Distance (yds)"]/90,0)

    df_final = df[["Person ID","Athlete Name","Athlete Position","Athlete Groups","Start Date","Start Time","Start Time (s)",
                "End Time (s)","Week Start Date","Month Start Date","Session Type","Tags","Segment Name","Duration (minutes)",
                "Session Load","Distance (yds)","Yards per Minute (yds)","High Intensity Running (yds)","No. of High Intensity Events",
                "Sprint Distance (yds)","No. of Sprints", "Top Speed (mph)","Avg Speed (mph)", "Accelerations","Decelerations","Percentage of Max Speed"]]


    print('\nSave Demo GPS Data to CSV')
    if model:
        out_file = data_dir_demo / 'gps_data_raw_model.csv'
    else:
        out_file = data_dir_demo / 'gps_data_raw_current.csv'
    df_final.to_csv(out_file,index=False)

    return df_final

###########################################################################
def injury_demo(gps_data):
    overuse_flag = ['Y','N']
    weights = [0.6,0.4]

    injury_sample_raw = gps_data.sample(n=40, random_state=19).reset_index(drop=True)
    injury_sample = injury_sample_raw[['Athlete Name','Start Date']]
    injury_sample = injury_sample.rename(columns={"Athlete Name":"Patient","Start Date":"Injury Date"})

    injury_sample["Overuse Injury"] = np.random.choice(overuse_flag, size=len(injury_sample), p=weights)

    print('\nSave Demo Injury Data to CSV')
    out_file = data_dir_demo / 'injury_data_raw.csv'
    injury_sample.to_csv(out_file,index=False)

    return injury_sample



###########################################################################
# Generate Demo Data

# Model Data 2024
gps_demo_df_model = gps_demo(dates_model,True)
injury_demo_df = injury_demo(gps_demo_df_model)

# Current Season 2025
gps_demo_df_current = gps_demo(dates_current,False)





