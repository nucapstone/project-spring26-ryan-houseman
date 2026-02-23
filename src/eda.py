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
data_dir = root / 'data'

############################################################################
# Upload Raw GPS Data
print('Upload Combined Dataset')
# Raw GPS Data
bms_data_file = data_dir / 'bms_data_2026.csv'
bms_data = pd.read_csv(bms_data_file)


###########################################################################

# Convert Dates to Datetime and Sort
bms_data['date'] = pd.to_datetime(bms_data['date'])

bms_data = bms_data.sort_values('date')

###########################################################################

# Aggregated Data by Player (sum)
aggs = bms_data.groupby(['player_name'],as_index=False)[['duration','load','distance','high_intensity_yards','high_intensity_events','sprint_distance','sprints','accelerations','decelerations']].sum()
# Sorted Results by Player
sorted_dist_s = aggs.sort_values('distance',ascending=False)['player_name']


# Aggregated Data by Player (avg)
aggm = bms_data.groupby(['player_name'],as_index=False)[['duration','load','distance','yards_per_minute','high_intensity_yards','high_intensity_events','sprint_distance','sprints','top_speed','avg_speed','accelerations','decelerations','percent_max_speed']].mean()
# Sorted Results by Player
sorted_dist_m = aggm.sort_values('distance',ascending=False)['player_name']

##############################################################################
# Generate EDA Plots

from plotting import bms_scatter, facet_barplot, bms_lineplot # type: ignore


# Scatterplots
bms_scatter(bms_data,'distance','sprints','session_type','Total Distance vs # of Sprints by Session Type','Distance Covered (yds)','# of Sprints',True,'figures/eda/scatter_distance_sprints.png',False)
bms_scatter(bms_data,'top_speed','distance','session_type','Top Speed vs Distance','Top Speed (mph)','Distance Covered (yds)',True,'figures/eda/scatter_topspeed_distance.png',False)
bms_scatter(bms_data,'accelerations','decelerations','session_type','Accelerations vs Decelerations by Session Type','# of Accelerations','# of Decelerations',True,'figures/eda/scatter_accelerations_decelerations.png',True)

# # Facetbarplots
facet_barplot(bms_data,aggs,'distance',player_colors,sum,'Total Player Distance by Session Type','Distance Covered (yds)',True,'figures/eda/barplot_distance.png')
facet_barplot(bms_data,aggs,'high_intensity_yards',player_colors,sum,'Player High Intensity Yards by Session Type','High Intensity Distance Covered (yds)',True,'figures/eda/barplot_high_intensity.png')
facet_barplot(bms_data,aggm,'yards_per_minute',player_colors,np.mean,'Player Yards per Minute by Session Type','Yards per Minute',True,'figures/eda/yards_per_minute.png')


# Trend Lines
bms_lineplot(bms_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,'figures/eda/trend_yards_per_minute_ishibashi',True,'Keito Ishibashi',False,player_colors)
bms_lineplot(bms_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,'figures/eda/trend_yards_per_minute_prince',True,'Adam Prince',True,player_colors)
bms_lineplot(bms_data,'yards_per_minute','session_type','Trend of Yards per Minute by Session Type','Date','Yards Covered per Minute',True,'figures/eda/trend_yards_per_minute_session',True,None,False,match_colors)


##############################################################################

# Dimensionality Reduction (PCA & T-SNE)


##############################################################################