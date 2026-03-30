import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

from color_palette import player_colors, match_colors, position_colors #type: ignore


# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir_actual = root / 'data/actual'
data_dir_demo = root / 'data/demo'

# Check if there is any actual data to use, otherwise use the demo data
# files = [f for f in os.listdir(primary_dir) if f.endswith(".csv")]
# if files:
#     data_dir = data_dir_actual
#     demo=False
# else:
#     data_dir = data_dir_demo
#     demo=True

#######################################
# Test Demo Data
data_dir = data_dir_demo
demo=True

############################################################################
# Upload Raw GPS Data
print('Upload Combined Dataset')
# Raw GPS Data
data_file = data_dir / 'prepped_data.csv'
gps_data = pd.read_csv(data_file)


###########################################################################

# Convert Dates to Datetime and Sort
gps_data['date'] = pd.to_datetime(gps_data['date'])

gps_data = gps_data.sort_values('date')

###########################################################################

# Aggregated Data by Player (sum)
aggs = gps_data.groupby(['player_name'],as_index=False)[['duration','load','distance','high_intensity_yards','high_intensity_events','sprint_distance','sprints','accelerations','decelerations']].sum()
# Sorted Results by Player
sorted_dist_s = aggs.sort_values('distance',ascending=False)['player_name']


# Aggregated Data by Player (avg)
aggm = gps_data.groupby(['player_name'],as_index=False)[['duration','load','distance','yards_per_minute','high_intensity_yards','high_intensity_events','sprint_distance','sprints','top_speed','avg_speed','accelerations','decelerations','percent_max_speed']].mean()
# Sorted Results by Player
sorted_dist_m = aggm.sort_values('distance',ascending=False)['player_name']

##############################################################################
# Generate EDA Plots

from plotting import gps_scatter, facet_barplot, gps_lineplot # type: ignore

if demo:
    figures_prefix = 'figures/eda/demo/'
else:
    figures_prefix = 'figures/eda/actual/'

# Scatterplots
gps_scatter(gps_data,'distance','sprints','session_type','Total Distance vs # of Sprints by Session Type','Distance Covered (yds)','# of Sprints',True,f'{figures_prefix}scatter_distance_sprints.png',False)
gps_scatter(gps_data,'top_speed','distance','session_type','Top Speed vs Distance','Top Speed (mph)','Distance Covered (yds)',True,f'{figures_prefix}scatter_topspeed_distance.png',False)
gps_scatter(gps_data,'accelerations','decelerations','session_type','Accelerations vs Decelerations by Session Type','# of Accelerations','# of Decelerations',True,f'{figures_prefix}scatter_accelerations_decelerations.png',True)

# # Facetbarplots
facet_barplot(gps_data,aggs,'distance',player_colors,sum,'Total Player Distance by Session Type','Distance Covered (yds)',True,f'{figures_prefix}barplot_distance.png')
facet_barplot(gps_data,aggs,'high_intensity_yards',player_colors,sum,'Player High Intensity Yards by Session Type','High Intensity Distance Covered (yds)',True,f'{figures_prefix}barplot_high_intensity.png')
facet_barplot(gps_data,aggm,'yards_per_minute',player_colors,np.mean,'Player Yards per Minute by Session Type','Yards per Minute',True,f'{figures_prefix}yards_per_minute.png')


# Trend Lines

# Bowdoin Players
#bms_lineplot(gps_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,f'{figures_prefix}trend_yards_per_minute_ishibashi',True,'Keito Ishibashi',False,player_colors)
#bms_lineplot(gps_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,f'{figures_prefix}trend_yards_per_minute_prince',True,'Adam Prince',True,player_colors)


# Demo Data
gps_lineplot(gps_data,'yards_per_minute','session_type','Trend of Yards per Minute by Session Type','Date','Yards Covered per Minute',True,f'{figures_prefix}trend_yards_per_minute_session',True,None,False,match_colors)
gps_lineplot(gps_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,f'{figures_prefix}trend_yards_per_minute_player_a',True,'Player A',False,player_colors)
gps_lineplot(gps_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,f'{figures_prefix}trend_yards_per_minute_player_r',True,'Player R',True,player_colors)


##############################################################################

# Dimensionality Reduction (PCA & T-SNE)


##############################################################################