import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import os

# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir_actual = root / 'data/actual'
data_dir_demo = root / 'data/demo'

# Check if there is any actual data to use, otherwise use the demo data
files = [f for f in os.listdir(data_dir_actual) if f.endswith(".csv")]
if files:
    data_dir = data_dir_actual
    demo=False
else:
    data_dir = data_dir_demo
    demo=True

if demo:
    print('\nData Pipeline using Demo Data')
else:
    print('\nData Pipeline using Actual GPS & Injury Data ')

#######################################
#Test Demo Data
# data_dir = data_dir_demo
# demo=True

####################################################################################################################################
# 1. Model Data
print('\nData Prep for Model Generation Data')

############################################################################
# Upload Raw GPS Data
print('Upload Raw GPS Data - Model')
# Raw GPS Data
raw_gps_file = data_dir / 'gps_data_raw.csv'

gps_data_raw = pd.read_csv(raw_gps_file)
print(gps_data_raw.head())

############################################################################
# Remove records without any output metrics
print('\nClean the Raw GPS Data')
gps = gps_data_raw.dropna(subset=['Duration (minutes)'])
gps = gps[gps['Session Load'] != 0].reset_index(drop=True)
gps = gps[gps['Segment Name'] == 'Whole Session'].reset_index(drop=True)
gps = gps[gps['Percentage of Max Speed'] != 0].reset_index(drop=True)
gps = gps[gps['Distance (yds)'] >= 100].reset_index(drop=True)

# Drop unneccesary columsn
gps = gps.drop(['Start Time','Person ID','Athlete Groups','Week Start Date','Month Start Date','Tags','Segment Name'],axis=1)

# Rename Columns
gps.rename(columns={'Person ID':'player_id','Athlete Name':'player_name','Athlete Position':'position','Athlete Groups':'player_group',
                               'Start Date':'date','Start Time (s)':'start_time', 'End Time (s)': 'end_time','Week Start Data':'week','Month Start Date':'month',
                               'Session Type':'session_type','Tags':'tags','Segment Name':'segment','Duration (minutes)':'duration','Session Load':'load',
                               'Distance (yds)':'distance','Yards per Minute (yds)':'yards_per_minute','High Intensity Running (yds)':'high_intensity_yards',
                               'No. of High Intensity Events':'high_intensity_events','Sprint Distance (yds)':'sprint_distance','No. of Sprints':'sprints',
                               'Top Speed (mph)':'top_speed','Avg Speed (mph)':'avg_speed','Accelerations':'accelerations','Decelerations':'decelerations',
                               'Percentage of Max Speed':'percent_max_speed'}, inplace=True)

# Convert GPS data to datetime
gps['date'] = pd.to_datetime(gps['date'],format='mixed',dayfirst=False)


###########################################################################
# Upload injury data
print('\nUpload & Clean Raw Injury Data')
# Raw GPS Data
raw_injuries_file = data_dir / 'injury_data_raw.csv'

injuries_raw = pd.read_csv(raw_injuries_file)

########################################################################################
# Updates to scructure of raw injury data
# # Rename Columns
injuries = injuries_raw.copy()

injuries.rename(columns={'Patient':'player_name_raw','Overuse Injury':'overuse_flag',
                               'Injury Date':'injury_date'}, inplace=True)


# Convert Injury Date to DateTime
injuries['injury_date'] = pd.to_datetime(injuries['injury_date'],format='mixed',dayfirst=False)

############################################################################################

# Fix Player Names
def player_name_update(name):
    first_last = name.split(",")
    player_name = first_last[1][1:] + ' ' + first_last[0]
    return player_name

if not demo:
    injuries['player_name'] = injuries['player_name_raw'].apply(player_name_update)
    injuries = injuries.drop('player_name_raw',axis=1)
    injuries['injury_flag'] = 1
else:
    injuries['player_name'] = injuries['player_name_raw']
    injuries = injuries.drop('player_name_raw',axis=1)
    injuries['injury_flag'] = 1


###########################################################################

# Link in Injury Data
print('\nLink Injury Data to GPS Data & Add Flags for Injury Occurences')

#Flag for Any Injury During Season'
any_injury = injuries.groupby(['player_name'],as_index=False)[['injury_flag']].max()
dataset = pd.merge(gps,any_injury,how='left',on='player_name')

dataset['injury_season'] = dataset['injury_flag']
dataset.drop('injury_flag',axis=1,inplace=True)
dataset = dataset.fillna(0)

#Flag for Any Overuse Injury During Season'
overuse_injuries = injuries.loc[injuries['overuse_flag'] == 'Y',]
any_overuse_injury = overuse_injuries.groupby(['player_name'],as_index=False)[['injury_flag']].max()
dataset = pd.merge(dataset,any_overuse_injury,how='left',on='player_name')

dataset['overuse_injury_season'] = dataset['injury_flag']
dataset.drop('injury_flag',axis=1,inplace=True)
dataset = dataset.fillna(0)


# Define Minimized GPS Data for joining Injuries by date
gps_min = gps[['player_name','date','start_time','end_time','session_type']]

def flag_injuries_time(dataset, overuse, date_compare,output_col):
    gps = gps_min.copy()
    if overuse:
        inj = overuse_injuries.copy()
    else:
        inj = injuries.copy()
    df_cmb = pd.merge(gps,inj,how='left',on='player_name')
    df_cmb[output_col] = df_cmb.apply(date_compare,axis=1)
    df_cmb_agg = df_cmb.groupby(['player_name','date','start_time','end_time','session_type'],as_index=False)[[output_col]].max()

    dataset = pd.merge(dataset,df_cmb_agg,how='left',on=['player_name','date','start_time','end_time','session_type'])
    return dataset

#Flag for Any Injury Previously Incurred During Season'
def prev_injury(row):
    if (row['date'] > row['injury_date']) and row['injury_flag'] == 1:
        return 1
    else:
        return 0
dataset = flag_injuries_time(dataset,False,prev_injury,'previous_injury')

#Flag for Any Injury Previously Incurred Overuse During Season'
dataset = flag_injuries_time(dataset,True,prev_injury,'previous_overuse_injury')


#Flag for Any Injury Incurred on the same Day'
def injury_day(row):
    if (row['date'] == row['injury_date']) and row['injury_flag'] == 1:
        return 1
    else:
        return 0
dataset = flag_injuries_time(dataset,False,injury_day,'injury_day')

#Flag for Any Overuse Injury Incurred on the same Day'
dataset = flag_injuries_time(dataset,True,injury_day,'overuse_injury_day')

#Flag for Any Injury Incurred within prior 1 week'
def injury_prior_week(row):
    if (row['date'] > row['injury_date']) and (row['date'] - row['injury_date'] <= pd.Timedelta(days=7)) and row['injury_flag'] == 1:
        return 1
    else:
        return 0
dataset = flag_injuries_time(dataset,False,injury_prior_week,'injury_prior_week')

#Flag for Any Overuse Injury Incurred within prior 1 week'
dataset = flag_injuries_time(dataset,True,injury_prior_week,'overuse_injury_prior_week')

#Flag for Any Injury Incurred within upcoming 1 week or day of'
def injury_upcoming_week(row):
    if (row['date'] <= row['injury_date']) and (row['injury_date'] - row['date'] <= pd.Timedelta(days=7)) and row['injury_flag'] == 1:
        return 1
    else:
        return 0
dataset = flag_injuries_time(dataset,False,injury_upcoming_week,'injury_upcoming_week')

#Flag for Any Overuse Injury Incurred within upcoming 1 week'
dataset = flag_injuries_time(dataset,True,injury_upcoming_week,'overuse_injury_upcoming_week')

#Flag for Any Injury Incurred within upcoming 10 days'
def injury_upcoming_10d(row):
    if (row['date'] <= row['injury_date']) and (row['injury_date'] - row['date'] <= pd.Timedelta(days=10)) and row['injury_flag'] == 1:
        return 1
    else:
        return 0
dataset = flag_injuries_time(dataset,False,injury_upcoming_10d,'injury_upcoming_10d')

#Flag for Any Overuse Injury Incurred within upcoming 10 days'
dataset = flag_injuries_time(dataset,True,injury_upcoming_10d,'overuse_injury_upcoming_10d')

#########################################################################
# Add One Hot Encoders for Athlete Position & Session Type
print('\nAdd One Hot Encoder for Categorical Variables (Position & Session Type)')

categorical_cols = ['position','session_type']
encoder = OneHotEncoder(sparse_output=False,handle_unknown='ignore')

encoded_array = encoder.fit_transform(dataset[categorical_cols])

encoded_cols = encoder.get_feature_names_out(categorical_cols)
encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=dataset.index)

dataset = pd.concat([dataset,encoded_df],axis=1)

# Rename Columns
dataset.rename(columns={'position_Centre Attacking Midfielder':'position_center_attacking_midfielder','position_Centre Back':'position_center_back','position_Centre Defensive Midfielder':'position_center_defensive_midfielder',
                        'position_Centre Midfielder':'position_center_midfielder','position_Goalkeeper':'position_goalkeeper', 'position_Left Back':'position_left_back',
                        'position_Right Back':'position_right_back','position_Right Midfielder':'position_right_midfielder','position_Striker':'position_striker', 
                        'position_Center Back':'position_center_back', 'position_Center Midfielder':'position_center_midfielder','position_Outside Back':'position_outside_back', 'position_Outside Midfielder':'position_outside_midfielder',
                        'session_type_Match Session':'session_type_match','session_type_Training Session':'session_type_training'}, inplace=True)


# Create player IDs
unique_players = dataset['player_name'].unique()
player_to_id = {cat: round(idx+100000,0) for idx, cat in enumerate(unique_players)}

# Step 2: Map categories to IDs
dataset['player_id'] = dataset['player_name'].map(player_to_id)

#########################################################################
print('\nCombinded Dataset Description')
description = dataset.describe()
print(description)

###########################################################################
# Format Date for output
dataset['date'] = pd.to_datetime(dataset['date']).dt.strftime('%Y-%m-%d')
###########################################################################
print('\nSave Combinded Data to CSV')
cmb_file = data_dir / 'prepped_data.csv'
dataset.to_csv(cmb_file,index=False)

###########################################################################

####################################################################################################################################
# 1. Current Season Data
print('\nData Prep for Current Season Data')

############################################################################
# Upload Raw GPS Data
print('Upload Raw GPS Data - Current Season')
# Raw GPS Data
raw_gps_file_c = data_dir / 'gps_data_raw_current.csv'

gps_data_raw_c = pd.read_csv(raw_gps_file_c)

############################################################################
# Remove records without any output metrics
print('\nClean the Raw GPS Data')
gps_c = gps_data_raw_c.dropna(subset=['Duration (minutes)'])
gps_c = gps_c[gps_c['Session Load'] != 0].reset_index(drop=True)
gps_c = gps_c[gps_c['Segment Name'] == 'Whole Session'].reset_index(drop=True)
gps_c = gps_c[gps_c['Percentage of Max Speed'] != 0].reset_index(drop=True)
gps_c = gps_c[gps_c['Distance (yds)'] >= 100].reset_index(drop=True)

# Drop unneccesary columsn
gps_c = gps_c.drop(['Start Time','Person ID','Athlete Groups','Week Start Date','Month Start Date','Tags','Segment Name'],axis=1)

# Rename Columns
gps_c.rename(columns={'Person ID':'player_id','Athlete Name':'player_name','Athlete Position':'position','Athlete Groups':'player_group',
                               'Start Date':'date','Start Time (s)':'start_time', 'End Time (s)': 'end_time','Week Start Data':'week','Month Start Date':'month',
                               'Session Type':'session_type','Tags':'tags','Segment Name':'segment','Duration (minutes)':'duration','Session Load':'load',
                               'Distance (yds)':'distance','Yards per Minute (yds)':'yards_per_minute','High Intensity Running (yds)':'high_intensity_yards',
                               'No. of High Intensity Events':'high_intensity_events','Sprint Distance (yds)':'sprint_distance','No. of Sprints':'sprints',
                               'Top Speed (mph)':'top_speed','Avg Speed (mph)':'avg_speed','Accelerations':'accelerations','Decelerations':'decelerations',
                               'Percentage of Max Speed':'percent_max_speed'}, inplace=True)

# Convert GPS data to datetime
gps_c['date'] = pd.to_datetime(gps_c['date'],format='mixed',dayfirst=False)

dataset_c = gps_c.copy()
#########################################################################
# Add One Hot Encoders for Athlete Position & Session Type
print('\nAdd One Hot Encoder for Categorical Variables (Position & Session Type)')

categorical_cols = ['position','session_type']
encoder = OneHotEncoder(sparse_output=False,handle_unknown='ignore')

encoded_array = encoder.fit_transform(dataset_c[categorical_cols])

encoded_cols = encoder.get_feature_names_out(categorical_cols)
encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=dataset_c.index)

dataset_c = pd.concat([dataset_c,encoded_df],axis=1)

# Rename Columns
dataset_c.rename(columns={'position_Centre Attacking Midfielder':'position_center_attacking_midfielder','position_Centre Back':'position_center_back','position_Centre Defensive Midfielder':'position_center_defensive_midfielder',
                        'position_Centre Midfielder':'position_center_midfielder','position_Goalkeeper':'position_goalkeeper', 'position_Left Back':'position_left_back',
                        'position_Right Back':'position_right_back','position_Right Midfielder':'position_right_midfielder','position_Striker':'position_striker', 
                        'position_Center Back':'position_center_back', 'position_Center Midfielder':'position_center_midfielder','position_Outside Back':'position_outside_back', 'position_Outside Midfielder':'position_outside_midfielder',
                        'session_type_Match Session':'session_type_match','session_type_Training Session':'session_type_training'}, inplace=True)


# Map Player IDs using the same mapping as above
# Step 2: Map categories to IDs
dataset_c['player_id'] = dataset_c['player_name'].map(player_to_id)

print(dataset_c.head())
###########################################################################
# Format Date for output
dataset_c['date'] = pd.to_datetime(dataset_c['date']).dt.strftime('%Y-%m-%d')
###########################################################################

print('\nSave Current Season GPS Data to CSV')
out_file = data_dir / 'prepped_data_current.csv'
dataset_c.to_csv(out_file,index=False)

###########################################################################