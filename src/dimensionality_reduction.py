import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import os


from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from sklearn.manifold import TSNE


# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir_actual = root / 'data/actual'
data_dir_demo = root / 'data/demo'

from color_palette import player_colors, match_colors, position_colors #type: ignore

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
# Test Demo Data
# data_dir = data_dir_demo
# demo=True

#################################################################################
# Upload Raw GPS Data
print('Upload Combined Dataset')
# Raw GPS Data
gps_data_file = data_dir / 'prepped_data.csv'
gps_data = pd.read_csv(gps_data_file)

#################################################################################
# Dimensionality Reduction (PCA & T-SNE)

#################################################################################

# Predictor Columns - With Categorical Encoders
if demo: 
    pca_cols = gps_data[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                        "accelerations","decelerations","percent_max_speed","position_center_midfielder","position_center_back",
                        "position_goalkeeper","position_outside_back","position_outside_midfielder","position_striker","session_type_match","session_type_training"
                        ]]

# Positions change slightly depending on demo data vs Bowdoin Data
else: 
    pca_cols = gps_data[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                        "accelerations","decelerations","percent_max_speed","position_center_attacking_midfielder","position_center_back","position_center_defensive_midfielder",
                        "position_center_midfielder","position_goalkeeper","position_left_back","position_right_back","position_striker","session_type_match","session_type_training"
                        ]]

# Predictor Columns - Without Categorical Encoders
pca_cols2 = gps_data[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                     "accelerations","decelerations","percent_max_speed"
                     ]]

# PCA
print('PCA')

gps_scaled = StandardScaler().fit_transform(pca_cols2)
pca = PCA(n_components=2)
pca_trnsfrm = pca.fit_transform(gps_scaled)

pca_out = pd.DataFrame(pca_trnsfrm)
pca_out.columns = ['PCA1','PCA2']
pca_out[['player_name','position','session_type']] = gps_data[['player_name','position','session_type']]
print(pca_out.head())

#################################################################################
# T-SNE
print('\nT-SNE')
tsne = TSNE(n_components=2, learning_rate= 200,perplexity=30,init='random',random_state=19)
bms_embedded = tsne.fit_transform(gps_scaled)

tsne_out = pd.DataFrame(bms_embedded)
tsne_out.columns = ['TSNE1','TSNE2']
tsne_out[['player_name','position','session_type']] = gps_data[['player_name','position','session_type']]
print(tsne_out.head())

#################################################################################

# Plot the Outputs
def dim_red_scatter(data,x,y,xlab,ylab,hue_dim,c_palette,title,fig_name,highlight, highlight_value):
    # Plot the output
    plt.figure(figsize=(8,6))
    if highlight:
        #sns.scatterplot(data=data, x=x, y=y, color='lightgray',alpha=0.4,legend=False)
        ax = sns.scatterplot(data=data, x=x, y=y, hue=hue_dim, palette={cat:'lightgray' for cat in hue_dim.unique()},alpha=0.4,legend=False)
        sns.scatterplot(data=data[hue_dim==highlight_value], x=x, y=y, hue=hue_dim, palette=c_palette,alpha=0.8,s=64)
        handles, labels = ax.get_legend_handles_labels()
        new_handles = [h for h, l in zip(handles, labels) if l in [highlight_value]]
        new_labels = [l for l in labels if l in [highlight_value]]
        ax.legend(new_handles, new_labels)

    else:
        ax = sns.scatterplot(data=data,x=x,y=y,hue=hue_dim,palette=c_palette,alpha=0.4,legend=True)
    
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.tight_layout()
    plt.savefig(fig_name)
    return

#################################################################################
print('\nGenerating Dimensionality Reduction Plots')

if demo:
    figures_prefix = 'figures/dimensionality_reduction/demo/'
else:
    figures_prefix = 'figures/dimensionality_reduction/actual/'

# PCA Plots
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['player_name'] ,player_colors,'GPS Data PCA - Player', f'{figures_prefix}pca_player.png',False,'None')
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['position'] ,position_colors,'GPS Data PCA - Position', f'{figures_prefix}pca_position.png',False,'None')
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['session_type'] ,match_colors,'GPS Data PCA - Session Type', f'{figures_prefix}pca_session_type.png',False,'None')


# highlighted PCA
##########################################################
# DELETE?
##########################################################
# Bowdoin Player
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['player_name'] ,player_colors,'GPS Data PCA - Tyler Huck', f'{figures_prefix}pca_player_huck.png',True,'Tyler Huck')

# Demo Data
# dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['player_name'] ,player_colors,'GPS Data PCA - Player F', f'{figures_prefix}pca_player_f.png',True,'Player F')
# dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['position'] ,position_colors,'GPS Data PCA - Goalkeeper', f'{figures_prefix}pca_position_goalkeeper.png',True,'Goalkeeper')


# T-SNE Plots
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', gps_data['player_name'] ,player_colors,'GPS Data T-SNE - Player', f'{figures_prefix}tsne_player.png',False, 'None')
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', gps_data['position'] ,position_colors,'GPS Data T-SNE - Position', f'{figures_prefix}tsne_position.png',False, 'None')
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', gps_data['session_type'] ,match_colors,'GPS Data T-SNE - Sessions Type', f'{figures_prefix}tsne_session.png',False, 'None')

##########################################################
# DELETE?
##########################################################
# Bowdoin Player
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', gps_data['player_name'] ,player_colors,'GPS Data T-SNE - Alden Mehta', f'{figures_prefix}tsne_player_mehta.png',True,'Alden Mehta')

# Demo Data
# dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', gps_data['player_name'] ,player_colors,'GPS Data T-SNE - Player C', f'{figures_prefix}tsne_player_c.png',True,'Player C')

dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', gps_data['position'] ,position_colors,'GPS Data T-SNE - Striker', f'{figures_prefix}tsne_position_striker.png',True,'Striker')
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', gps_data['session_type'] ,match_colors,'GPS Data T-SNE - Match Sessions', f'{figures_prefix}tsne_session_matches.png', True, 'Match Session')
