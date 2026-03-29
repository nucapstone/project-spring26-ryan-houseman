# File Used to Create a Database from Model Results

###########################################################################
from pathlib import Path
import numpy as np
import pandas as pd
import json

# import sqlite3
# from sqlite3 import Error

#################################################################################
# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir_actual = root / 'data/actual'
data_dir_demo = root / 'data/demo'
rpt_dir = root / 'reporting'
front_end_data = root / 'reporting/client/src/data'

# Check if there is any actual data to use, otherwise use the demo data
# if os.path.isdir(data_dir_actual) and os.listdir(data_dir_actual):
#     data_dir = data_dir_actual
#     demo=False
# else:
#     data_dir = data_dir_demo
#     demo=True

#######################################
# Test Demo Data
data_dir = data_dir_demo
demo=True

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

rslts_df['session_date'] = pd.to_datetime(rslts_df['session_date'],format='%Y-%m-%d',errors='coerce')
rslts_df['session_date'] = rslts_df['session_date'].dt.strftime('%Y-%m-%d')
rslts_df = rslts_df[['player_id','player_name','session_date','overuse_injury_day','injury_predicted_prob','injury_prediction','injury_flag','injury_flag_cnt','predicted_injury_flag_rate']]

##################################################################################
# Create JSON Array from Reporting Results

# Convert DataFrame to JSON string (array of objects)
json_rpt1 = rslts_df.to_json(orient='records')
rpt1_out = front_end_data / 'rpt1.json'

with open(rpt1_out, "w") as f:
    f.write(json_rpt1)

#################################################################################

# # Initialize Database 
# print('\nInitialize Database and populate with Model Results')
# sql_file = rpt_dir / 'schema.sql'
# with open(sql_file, 'r', encoding='utf-8') as f:
#             sql_script = f.read()
# db_path = rpt_dir / 'server/bms_gps.db'
# conn = sqlite3.connect(db_path)
# cursor = conn.cursor()
# cursor.executescript(sql_script)

# # Commit changes and close connection
# conn.commit()
# conn.close()

# def populate_db_from_df(db_path, table_name,df):
#   try:
#         print('Connect to Database')
#         # Connect to SQLite database
#         conn = sqlite3.connect(db_path)

#         # Append data to the table
#         df.to_sql(table_name, conn, if_exists='append', index=False)

#         inserted_rows = len(df)
#         print(f"Successfully inserted {inserted_rows} rows into '{table_name}'.")
#         return None

#   except Error as e:
#       print(f"SQLite error: {e}")
#       return

# populate_db_from_df(db_path,'model_results',rslts_df)

#################################################################################
# Save results to Data folder

print('\nSave Database Input to CSV')
db_file = data_dir / 'rpt_prep.csv'
rslts_df.to_csv(db_file,index=False)