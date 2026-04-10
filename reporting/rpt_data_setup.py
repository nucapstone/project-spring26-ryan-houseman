# File Used to Create Front End Reporting JSON files from Model Results

###########################################################################
from pathlib import Path
import numpy as np
import pandas as pd
import json
import os

#################################################################################
# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir_actual = root / 'data/actual'
data_dir_demo = root / 'data/demo'
rpt_dir = root / 'reporting'
front_end_data = root / 'reporting/client/src/data'

# Check if there is any actual data to use, otherwise use the demo data
files = [f for f in os.listdir(data_dir_actual) if f.endswith(".csv")]
if files:
    data_dir = data_dir_actual
    demo=False
else:
    data_dir = data_dir_demo
    demo=True

#######################################
# Test Demo Data
# data_dir = data_dir_demo
# demo=True

################################################################################
# Model Choice
# Use logistic regression for now, but there is evidence random forests are better
model_input = 'model_results_lreg.csv'

#################################################################################
# Upload Model Results
print('Upload Model Results')
model_results_file = data_dir / model_input
rslts_df = pd.read_csv(model_results_file)


#################################################################################
# Prepare Reporting Dataset - Player Overview & Detail
print('\nPlayer Overview & Player Detail Reporting Data Generation')
# Calculate COUNT OF Datapoints flagged in the previous prediction window for Injury by Player

rslts_df['session_date'] = pd.to_datetime(rslts_df['date'])
rslts_df['injury_predicted_prob'] = round(rslts_df['injury_predicted_prob'],4)
rslts_df = rslts_df.sort_values(['player_name','date'])

time_delta = rslts_df['prediction_window'].max()

print(rslts_df.head())

print(f'\nCalculate # of Predicted Injury Flags from Past {time_delta} days')
# Calculate number of days in the previous prediction window that a player was flagged for injury
target_value = 1
def rolling_injury_count(g,days):
    if days == 10:
        wind = '10D'
    else:
        wind = '7D'
    result = (
        g.set_index('session_date')['injury_prediction']
         .rolling(wind)
         .apply(lambda s: (s == target_value).sum(), raw=False)
    )
    result.index = g.index  # restore original index before returning
    return result

rslts_df['injury_flag_cnt_window'] = (
    rslts_df.groupby('player_name', group_keys=False)
            .apply(rolling_injury_count, days=time_delta, include_groups=False)
)

# Calculate # of records from the previous prediction window
rslts_df['cnt'] = 1
def rolling_session_count(g,days):
    if days == 10:
        wind = '10D'
    else:
        wind = '7D'
    result = (
        g.set_index('session_date')['cnt']
         .rolling(wind)
         .apply(lambda s: (s == target_value).sum(), raw=False)
    )
    result.index = g.index  # restore original index before returning
    return result


rslts_df['session_cnt_window'] = (
    rslts_df.groupby('player_name', group_keys=False)
            .apply(rolling_session_count, days=time_delta, include_groups=False)
)


rslts_df.drop(['cnt','date'],axis=1,inplace=True)
rslts_df['predicted_injury_flag_rate_window'] = round(rslts_df['injury_flag_cnt_window']/rslts_df['session_cnt_window'],2)


#################################################################################
# Calculate Freshness Metric (injury likelihood scaled by exponential distribution)

lambda_decay = 0.3
# For each row, calculate the weighted sum of injury_predicted_prob over the past 7 days
def freshness_metric(df, date, player_id):
    # Get the past 7 days of data for this player
    past_7_days = df[
        (df["player_id"] == player_id) &
        (df["session_date"] <= date) &
        (df["session_date"] >= date - pd.Timedelta(days=7))
    ].copy()
    
    # Calculate how many days ago each row occurred
    past_7_days["days_ago"] = (date - past_7_days["session_date"]).dt.days
    
    # Apply exponential decay weight
    past_7_days["weight"] = np.exp(-lambda_decay * past_7_days["days_ago"])
    
    # Return weighted sum
    return round((past_7_days["injury_predicted_prob"] * past_7_days["weight"]).sum(),2)

# Apply to every row in the dataframe
rslts_df["player_freshness"] = rslts_df.apply(
    lambda row: freshness_metric(rslts_df, row["session_date"], row["player_id"]), axis=1
)

rslts_df["player_freshness"] = round(1000 * (1 - (rslts_df["player_freshness"] - rslts_df["player_freshness"].min()) / 
                               (rslts_df["player_freshness"].max() - rslts_df["player_freshness"].min())),2)

#################################################################################
# Calculate Average Distance, Top Speed and Percent Max Speed by player over course of season
# Distance
rslts_df["avg_distance"] = round(rslts_df.groupby("player_id")["distance"].transform("mean"),2)

# Top Speed
rslts_df["avg_top_speed"] = round(rslts_df.groupby("player_id")["top_speed"].transform("mean"),2)

# Percent Max Speed
rslts_df["avg_pcnt_max_speed"] = round(rslts_df.groupby("player_id")["percent_max_speed"].transform("mean"),2)

print(rslts_df.head())

#################################################################################

rslts_df['session_date'] = pd.to_datetime(rslts_df['session_date'],format='%Y-%m-%d',errors='coerce')
rslts_df['session_date'] = rslts_df['session_date'].dt.strftime('%Y-%m-%d')
rslts_df = rslts_df[['player_id','player_name','session_date','injury_predicted_prob','injury_prediction','injury_flag_cnt_window','predicted_injury_flag_rate_window','session_cnt_window','player_freshness','distance','top_speed','percent_max_speed','avg_distance','avg_top_speed','avg_pcnt_max_speed','prediction_threshold','prediction_window']]

##################################################################################
# Create Team Overview Reporting Dataset
print('Team Overview Reporting Data Generation')
team_rslts = rslts_df.groupby(['session_date','prediction_threshold','prediction_window'],as_index=False).agg({'injury_predicted_prob':'mean','injury_prediction':'sum','injury_flag_cnt_window':'sum','predicted_injury_flag_rate_window':'mean','session_cnt_window':'sum','player_freshness':'mean','distance':'mean','top_speed':'mean','percent_max_speed':'mean'})
team_rslts['team_injury_predicted_prob'] = round(team_rslts['injury_predicted_prob'],4)
team_rslts['team_freshness'] = round(team_rslts['player_freshness'],2)
team_rslts['team_predicted_injury_flag_rate_window'] = round(team_rslts['predicted_injury_flag_rate_window'],2)
team_rslts['distance'] = round(team_rslts['distance'],2)
team_rslts['top_speed'] = round(team_rslts['top_speed'],2)
team_rslts['pcnt_max_speed'] = round(team_rslts['percent_max_speed'],2)

team_rslts['avg_team_freshness'] = round(team_rslts['team_freshness'].mean(),2)
team_rslts['avg_team_injury_predicted_prob'] = round(team_rslts['team_injury_predicted_prob'].mean(),2)
team_rslts['avg_team_distance'] = round(team_rslts['distance'].mean(),2)
team_rslts['avg_team_top_speed'] = round(team_rslts['top_speed'].mean(),2)
team_rslts['avg_team_pcnt_max_speed'] = round(team_rslts['pcnt_max_speed'].mean(),2)


team_rslts.drop(['player_freshness','predicted_injury_flag_rate_window','injury_predicted_prob','percent_max_speed'],axis=1,inplace=True)
team_rslts.rename(columns={'injury_prediction':'predicted_injuries_cnt','session_cnt_window':'team_session_cnt_window'}, inplace=True)

print(team_rslts.head())


##################################################################################
# Create JSON Array from Reporting Results

# Convert DataFrame to JSON string (array of objects)
json_rpt1 = rslts_df.to_json(orient='records')
rpt1_out = front_end_data / 'rpt1.json'

with open(rpt1_out, "w") as f:
    f.write(json_rpt1)

json_rpt2 = team_rslts.to_json(orient='records')
rpt2_out = front_end_data / 'rpt2.json'

with open(rpt2_out, "w") as f:
    f.write(json_rpt2)

#################################################################################
# Save results to Data folder
print('\nSave Reporting Data')
rpt1_file = data_dir / 'rpt_prep_player.csv'
rslts_df.to_csv(rpt1_file,index=False)

rpt2_file = data_dir / 'rpt_prep_team.csv'
team_rslts.to_csv(rpt2_file,index=False)

