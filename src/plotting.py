# Plotting Functions to use in other scripts

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import pandas as pd

# Define Functions for Various Plots

#######################################################################################################
# EDA 

def gps_scatter(dataset,xvar,yvar,hue,plot_title,xlab,ylab,save_fig,fig_name,show_means):
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



def facet_barplot(dataset,agg,metric,cmap,estimator,title,axis_label,save_fig,fig_name):
    # # FacetGrid of Barplot of Player Metrics split out by Session Type
    if estimator == sum:
        sorted_metric = agg.sort_values(metric,ascending=False)['player_name']
    else:
        sorted_metric = agg.sort_values(metric,ascending=False)['player_name']

    g = sns.FacetGrid(data=dataset,col='session_type',margin_titles=True,despine=False,height=7.5,aspect=1.2)
    g.map_dataframe(sns.barplot, x=metric,y='player_name',estimator=estimator,hue='player_name',palette=cmap,orient='h',order=sorted_metric)
    g.set_axis_labels(axis_label,"Player Name")
    g.set_titles(['Match','Training Session'])
    g.figure.suptitle(title,fontsize=16,fontweight='semibold')
    g.figure.tight_layout()

    if save_fig:
        g.savefig(fig_name)
    return

def gps_lineplot(dataset,yvar,hue,plot_title,xlab,ylab,save_fig,fig_name,show_mean,highlight_player,highlight_injury,colors):
    # Build Scatter Plot
    plt.figure(figsize=(8,6))
    if hue == 'session_type' or hue == 'position':
        ax = sns.lineplot(data=dataset, x='date', y=yvar,hue=hue,palette=colors,linewidth=1.5,alpha=0.7)
    elif hue == 'player_name':
        ax = sns.lineplot(data=dataset, x='date', y=yvar, hue=hue, palette={cat:'lightgray' for cat in dataset['player_name'].unique()},linewidth=1.5,alpha=0.35,legend=False)
        sns.lineplot(data=dataset[dataset['player_name']==highlight_player], x='date', y=yvar, hue=hue, palette=colors,linewidth=2.5,alpha=1)
    else:
        ax = sns.lineplot(data=dataset, x='date', y=yvar, palette='Set2',linewidth=1.5,alpha=0.7)
    if show_mean:
        mean_y = dataset[yvar].mean()

        ax.axhline(mean_y,color='#4E4E52',linestyle='--',linewidth=1.5)
    
    if highlight_injury:
        injury_dates = dataset.loc[(dataset['overuse_injury_day'] == 1) & (dataset['player_name'] == highlight_player),'date']
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

############################################################################################################################
# Model Results
def output_lineplot(dataset,hue,plot_title,xlab,ylab,save_fig,fig_name,highlight_player,colors,risk_threshold):
    # Build Scatter Plot
    plt.figure(figsize=(8,6))
    ax = sns.lineplot(data=dataset, x='date', y='injury_predicted_prob', hue=hue, palette={cat:'lightgray' for cat in dataset['player_name'].unique()},linewidth=1.5,alpha=0.35,legend=False)
    sns.lineplot(data=dataset[dataset['player_name']==highlight_player], x='date', y='injury_predicted_prob', hue=hue, palette=colors,linewidth=2.5,alpha=1)

    # Highlight Injuries in Red lines & Shade week before
    injury_dates = dataset.loc[(dataset['overuse_injury_day'] == 1) & (dataset['player_name'] == highlight_player),'date'].unique()
    for day in injury_dates:
        ax.axvline(day,color='red',linestyle='--',linewidth=2)
        week_earlier = day - pd.Timedelta(weeks=1)
        plt.axvspan(week_earlier, day, color='red',alpha=0.1)

    # # Highlight Datapoints flagged for injury prediction
    injury_preds = dataset.loc[(dataset['injury_predicted_prob'] >= risk_threshold) & (dataset['player_name'] == highlight_player),['date','injury_predicted_prob']]
    injury_preds['date'] = pd.to_datetime(injury_preds['date'])
    injury_preds = injury_preds.sort_values('date')

    print('\n')
    print(injury_preds)

    plt.plot(injury_preds['date'],injury_preds['injury_predicted_prob'],'rx',markersize=6,label='Injury Likelihood Flagged')
    plt.axhline(risk_threshold,color='grey',linestyle='--',linewidth=1.5)

    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2)) # Show every 2 weeks
    plt.xticks(rotation=45)

    plt.title(plot_title,fontsize=16,fontweight='semibold')
    plt.xlabel(xlab,fontsize=14)
    plt.ylabel(ylab,fontsize=14)
    plt.tight_layout()

    if save_fig:
        plt.savefig(fig_name)
    plt.close()
    return

