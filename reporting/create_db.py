# File Used to Create a Database from Model Results

###########################################################################
from pathlib import Path
import numpy as np
import pandas as pd

import sqlite3
from sqlite3 import Error

#################################################################################
# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir = root / 'data'
rpt_dir = root / 'reporting'

#################################################################################
# Upload Model Results
print('Upload Model Results')
model_results_file = data_dir / 'model_results.csv'
rslts_df = pd.read_csv(model_results_file)

#################################################################################
# Calculate COUNT OF Datapoints flagged in the previous week for Injury by Player

rslts_df['session_date'] = pd.to_datetime(rslts_df['date'])
rslts_df['injury_predicted_prob'] = round(rslts_df['injury_predicted_prob'],4)
rslts_df = rslts_df.sort_values(['player_name','date'])

target_value = 1
rslts_df['injury_flag_cnt'] = (
    rslts_df.groupby(['player_name'],as_index=False)
      .apply(lambda g: g.set_index('session_date')
                        .rolling('7D')['injury_prediction']
                        .apply(lambda s: (s == target_value).sum(), raw=False),include_groups=False)
      .reset_index(level=0, drop=True)
      .values
)

rslts_df['cnt'] = 1
rslts_df['record_cnt'] = (
    rslts_df.groupby(['player_name'],as_index=False)
      .apply(lambda g: g.set_index('session_date')
                        .rolling('7D')['cnt']
                        .apply(lambda s: (s == target_value).sum(), raw=False),include_groups=False)
      .reset_index(level=0, drop=True)
      .values
)

rslts_df.drop(['cnt','date'],axis=1,inplace=True)
rslts_df['predicted_injury_flag_rate'] = round(rslts_df['injury_flag_cnt']/rslts_df['record_cnt'],4)
rslts_df.drop('record_cnt',axis=1,inplace=True)

print(rslts_df.head())

#################################################################################
# Create player IDs
unique_players = rslts_df['player_name'].unique()
player_to_id = {cat: idx+100000 for idx, cat in enumerate(unique_players)}

# Step 2: Map categories to IDs
rslts_df['player_id'] = rslts_df['player_name'].map(player_to_id)

rslts_df['session_date'] = pd.to_datetime(rslts_df['session_date'],format='%Y-%m-%d',errors='coerce')
rslts_df['session_date'] = rslts_df['session_date'].dt.strftime('%Y-%m-%d')
rslts_df = rslts_df[['player_id','player_name','session_date','overuse_injury_day','injury_predicted_prob','injury_prediction','injury_flag','injury_flag_cnt','predicted_injury_flag_rate']]

#################################################################################

# Initialize Database 
sql_file = rpt_dir / 'schema.sql'
with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
db_path = rpt_dir / 'server/bms_gps.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.executescript(sql_script)

# Commit changes and close connection
conn.commit()
conn.close()

def append_df_to_db(db_path, table_name,df):
  try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)

        # Append data to the table
        df.to_sql(table_name, conn, if_exists='append', index=False)

        inserted_rows = len(df)
        print(f"Successfully inserted {inserted_rows} rows into '{table_name}'.")
        return None

  except Error as e:
      print(f"SQLite error: {e}")
      return

#db_path = rpt_dir / '/server/bms_gps.db'
append_df_to_db(db_path,'model_results',rslts_df)

#################################################################################
# Save results to Data folder

print('\nSave Combinded Data to CSV')
db_file = data_dir / 'db_prep.csv'
rslts_df.to_csv(db_file,index=False)