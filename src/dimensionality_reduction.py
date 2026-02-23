import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import time


from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from sklearn.manifold import TSNE


# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir = root / 'data'

#################################################################################
# Upload Raw GPS Data
print('Upload Combined Dataset')
# Raw GPS Data
bms_data_file = data_dir / 'bms_data_2026.csv'
bms_data = pd.read_csv(bms_data_file)

# print(bms_data.head())
# for col in bms_data.columns:
#     print(col)


#################################################################################

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

match_colors = {
    "Training Session":"#66C2A5",
    "Match Session":"#FC8D62"
}

position_colors = {
    "Goalkeeper":"#66C2A5",
    "Right Midfielder":"#FC8D62",
    "Striker":"#8DA0CB",
    "Centre Back":"#E78AC3",
    "Left Back":"#A6D854",
    "Centre Attacking Midfielder":"#FFD92F",
    "Centre Midfielder":"#E5C494",
    "Right Back":"#B3B3B3",
    "Centre Defensive Midfielder":"#66C2A5"
}

#################################################################################
# Dimensionality Reduction (PCA & T-SNE)

#################################################################################

# Predictor Columns - With Categorical Encoders
pca_cols = bms_data[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                     "accelerations","decelerations","percent_max_speed","position_center_attacking_midfielder","position_center_back","position_center_defensive_midfielder",
                     "position_center_midfielder","position_goalkeeper","position_left_back","position_right_back","position_striker","session_type_match","session_type_training"
                     ]]

# Predictor Columns - Without Categorical Encoders
pca_cols2 = bms_data[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                     "accelerations","decelerations","percent_max_speed"
                     ]]

# PCA
print('PCA')

bms_scaled = StandardScaler().fit_transform(pca_cols2)
pca = PCA(n_components=2)
pca_trnsfrm = pca.fit_transform(bms_scaled)

pca_out = pd.DataFrame(pca_trnsfrm)
pca_out.columns = ['PCA1','PCA2']
pca_out[['player_name','position','session_type']] = bms_data[['player_name','position','session_type']]
print(pca_out.head())

#################################################################################
# T-SNE
print('\nT-SNE')
tsne = TSNE(n_components=2, learning_rate= 200,perplexity=30,init='random',random_state=19)
bms_embedded = tsne.fit_transform(bms_scaled)

tsne_out = pd.DataFrame(bms_embedded)
tsne_out.columns = ['TSNE1','TSNE2']
tsne_out[['player_name','position','session_type']] = bms_data[['player_name','position','session_type']]
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

# PCA Plots
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['player_name'] ,player_colors,'BMS GPS Data PCA - Player', 'figures/dimensionality_reduction/pca_player.png',False,'None')
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['position'] ,position_colors,'BMS GPS Data PCA - Position', 'figures/dimensionality_reduction/pca_position.png',False,'None')
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['session_type'] ,match_colors,'BMS GPS Data PCA - Session Type', 'figures/dimensionality_reduction/pca_session_type.png',False,'None')

# highlighted PCA
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['player_name'] ,player_colors,'BMS GPS Data PCA - Tyler Huck', 'figures/dimensionality_reduction/pca_player_huck.png',True,'Tyler Huck')
dim_red_scatter(pca_out,'PCA1','PCA2','1st Principal Component','2nd Principal Component', pca_out['position'] ,position_colors,'BMS GPS Data PCA - Goalkeeper', 'figures/dimensionality_reduction/pca_position_goalkeeper.png',True,'Goalkeeper')


# T-SNE Plots
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', bms_data['player_name'] ,player_colors,'BMS GPS Data T-SNE - Player', 'figures/dimensionality_reduction/tsne_player.png',False, 'None')
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', bms_data['position'] ,position_colors,'BMS GPS Data T-SNE - Position', 'figures/dimensionality_reduction/tsne_position.png',False, 'None')
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', bms_data['session_type'] ,match_colors,'BMS GPS Data T-SNE - Sessions Type', 'figures/dimensionality_reduction/tsne_session.png',False, 'None')

dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', bms_data['player_name'] ,player_colors,'BMS GPS Data T-SNE - Alden Mehta', 'figures/dimensionality_reduction/tsne_player_mehta.png',True,'Alden Mehta')
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', bms_data['position'] ,position_colors,'BMS GPS Data T-SNE - Left Backs', 'figures/dimensionality_reduction/tsne_position_left_back.png',True,'Left Back')
dim_red_scatter(tsne_out,'TSNE1','TSNE2','T-SNE Component 1','T-SNE Component 2', bms_data['session_type'] ,match_colors,'BMS GPS Data T-SNE - Match Sessions', 'figures/dimensionality_reduction/tsne_session_matches.png', True, 'Match Session')
