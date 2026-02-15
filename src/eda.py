import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


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


# ###########################################################################

# # Initial EDA
# Define Functions for Various Plots
def bms_scatter(dataset,xvar,yvar,hue,plot_title,xlab,ylab,save_fig,fig_name,show_means):
    # Build Scatter Plot
    plt.figure(figsize=(8,6))
    if hue != 'None':
        ax = sns.scatterplot(data=dataset, x=xvar, y=yvar,hue=hue,style=hue,palette='Set2',s=80,alpha=0.7)
    else:
        ax = sns.scatterplot(data=dataset, x=xvar, y=yvar,palette='Set2',s=80,alpha=0.7)

    if show_means:
        mean_x = dataset[xvar].mean()
        mean_y = dataset[yvar].mean()

        ax.axvline(mean_x,color='#4E4E52',linestyle='--',linewidth=1.5)
        ax.axhline(mean_y,color='#4E4E52',linestyle='--',linewidth=1.5)
    
    plt.title(plot_title,fontsize=16,fontweight='semibold')
    plt.xlabel(xlab,fontsize=14)
    plt.ylabel(ylab,fontsize=14)
    plt.tight_layout()

    if save_fig:
        plt.savefig(fig_name)
    return



def facet_barplot(dataset,metric,cmap,estimator,title,axis_label,save_fig,fig_name):
    # # FacetGrid of Barplot of Player Metrics split out by Session Type
    if estimator == sum:
        sorted_metric = aggs.sort_values(metric,ascending=False)['player_name']
    else:
        sorted_metric = aggm.sort_values(metric,ascending=False)['player_name']

    g = sns.FacetGrid(data=dataset,col='session_type',margin_titles=True,despine=False,height=7.5,aspect=1.2)
    g.map_dataframe(sns.barplot, x=metric,y='player_name',estimator=estimator,hue='player_name',palette=cmap,orient='h',order=sorted_metric)
    g.set_axis_labels(axis_label,"Player Name")
    g.set_titles(['Match','Training Session'])
    g.figure.suptitle(title,fontsize=16,fontweight='semibold')
    g.figure.tight_layout()

    if save_fig:
        g.savefig(fig_name)
    return

def bms_lineplot(dataset,yvar,hue,plot_title,xlab,ylab,save_fig,fig_name,show_mean,highlight_player,highlight_injury):
    # Build Scatter Plot
    plt.figure(figsize=(8,6))
    if hue == 'session_type':
        ax = sns.lineplot(data=dataset, x='date', y=yvar,hue=hue,palette='Set2',linewidth=1.5,alpha=0.7)
    elif hue == 'player_name':
        ax = sns.lineplot(data=dataset, x='date', y=yvar, hue=hue, palette={cat:'lightgray' for cat in dataset['player_name'].unique()},linewidth=1.5,alpha=0.35,legend=False)
        sns.lineplot(data=dataset[dataset['player_name']==highlight_player], x='date', y=yvar, hue=hue, palette=player_colors,linewidth=2.5,alpha=1)
    else:
        ax = sns.lineplot(data=dataset, x='date', y=yvar, palette='Set2',linewidth=1.5,alpha=0.7)
    if show_mean:
        mean_y = dataset[yvar].mean()

        ax.axhline(mean_y,color='#4E4E52',linestyle='--',linewidth=1.5)
    
    if highlight_injury:
        injury_dates = dataset.loc[(dataset['injury_day'] == 1) & (dataset['player_name'] == highlight_player),'date']
        for day in injury_dates:
            ax.axvline(day,color='red',linestyle='--',linewidth=1)
    
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2)) # Show every 2 weeks
    plt.xticks(rotation=45)

    plt.title(plot_title,fontsize=16,fontweight='semibold')
    plt.xlabel(xlab,fontsize=14)
    plt.ylabel(ylab,fontsize=14)
    plt.tight_layout()

    if save_fig:
        plt.savefig(fig_name)
    return

# Define Color Mapping for All Players - Using Set2 Palette
player_colors = {
    "Keito Ishibashi":"#66C2A5",
    "Jack Banks":"#FC8D62",
    "Liam Myers":"#8DA0CB",
    "Tyler Huck":"#E78AC3",
    "Adam Prince":"#A6D854",
    "William Fowler":"#FFD92F",
    "Mateo Pacelli":"#E5C494",
    "Luke Peltz":"#B3B3B3",
    "Alden Mehta":"#66C2A5",
    "Cade Priestap":"#FC8D62",
    "Paul Surkov":"#8DA0CB",
    "Max Cook":"#E78AC3",
    "Oliver Bruce":"#A6D854",
    "Liam Elias":"#FFD92F",
    "Arthur Dos Santos":"#E5C494",
    "Stefan Zehnacker":"#B3B3B3",
    "Alexander Ainsworth":"#66C2A5",
    "Donovan Sinicropi":"#FC8D62",
    "Kamar Burris-Khan":"#8DA0CB",
    "Sam Ames":"#E78AC3",
    "Felipe Rueda Duran":"#A6D854",
    "Masai Gordon":"#FFD92F",
    "Lucas Nuernberg":"#E5C494",
    "Oliver King":"#B3B3B3",
    "Jasper Peters":"#66C2A5",
    "Jonathan Perez":"#FC8D62",
    "Patrick Ritter":"#8DA0CB"
}

##############################################################################

# Generate Some Plots from Functions Above

# Scatterplots
bms_scatter(bms_data,'distance','sprints','session_type','Total Distance vs # of Sprints by Session Type','Distance Covered (yds)','# of Sprints',True,'figures/scatter_distance_sprints.png',False)
bms_scatter(bms_data,'top_speed','distance','session_type','Top Speed vs Distance','Top Speed (mph)','Distance Covered (yds)',True,'figures/scatter_topspeed_distance.png',False)
bms_scatter(bms_data,'accelerations','decelerations','session_type','Accelerations vs Decelerations by Session Type','# of Accelerations','# of Decelerations',True,'figures/scatter_accelerations_decelerations.png',True)

# # Facetbarplots
facet_barplot(bms_data,'distance',player_colors,sum,'Total Player Distance by Session Type','Distance Covered (yds)',True,'figures/barplot_distance.png')
facet_barplot(bms_data,'high_intensity_yards',player_colors,sum,'Player High Intensity Yards by Session Type','High Intensity Distance Covered (yds)',True,'figures/barplot_high_intensity.png')
facet_barplot(bms_data,'yards_per_minute',player_colors,np.mean,'Player Yards per Minute by Session Type','Yards per Minute',True,'figures/yards_per_minute.png')


# Trend Lines
bms_lineplot(bms_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,'figures/trend_yards_per_minute_ishibashi',True,'Keito Ishibashi',False)
bms_lineplot(bms_data,'yards_per_minute','player_name','Trend of Yards per Minute by Player','Date','Yards Covered per Minute',True,'figures/trend_yards_per_minute_prince',True,'Adam Prince',True)
bms_lineplot(bms_data,'yards_per_minute','session_type','Trend of Yards per Minute by Session Type','Date','Yards Covered per Minute',True,'figures/trend_yards_per_minute_session',True,None,False)


##############################################################################

# Dimensionality Reduction (PCA & T-SNE)


##############################################################################

# # Scatter Plot of Distance vs # of Sprints
# sns.scatterplot(data=bms_data, x="distance", y="sprints",hue="session_type",palette='Set2')
# plt.show()


# # Bar plot of Total Distance by Player
# plt.figure(figsize=(6,10))
# sns.barplot(x='distance',y='player_name',data=bms_data,estimator=sum,hue='player_name',palette='Set2',orient='h')

# plt.title("Total Distance by Player",fontsize=16)
# plt.ylabel("Player Name",fontsize=12)
# plt.xlabel("Total Distance (yds)",fontsize=12)

# plt.tight_layout()
# plt.show()


# # FacetGrid of Barplot Above Split out by Session Type
# g = sns.FacetGrid(data=bms_data,col='session_type',margin_titles=True,despine=False,height=8,aspect=1.2)
# g.map_dataframe(sns.barplot, x='distance',y='player_name',estimator=sum,hue='player_name',palette='Set2',orient='h',order=sorted_dist_s)
# g.set_axis_labels("Total Distance (yds)","Player Name")
# g.set_titles(['Match','Training Session'])
# plt.tight_layout()
# plt.show()


# # FacetGrid of Barplot Mean Distance by Player by Session Type
# g = sns.FacetGrid(data=bms_data,col='session_type',margin_titles=True,despine=False,height=8,aspect=1.2)
# g.map_dataframe(sns.barplot, x='distance',y='player_name',estimator=np.mean,hue='player_name',palette='Set2',orient='h',order=sorted_dist_m)
# g.set_axis_labels("Average Distance (yds)","Player Name")
# g.set_titles(['Match','Training Session'])
# plt.tight_layout()
# plt.show()