# Logistic Regression Model Implementation

###########################################################################
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import seaborn as sns
import matplotlib.pyplot as plt

#################################################################################
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

#################################################################################
# Upload Raw GPS Data
print('Upload Combined Dataset')
# Raw GPS Data
gps_data_file = data_dir / 'prepped_data.csv'
gps_data = pd.read_csv(gps_data_file)


#################################################################################
# Run PCA on GPS Data
# GPS Columns without Encoders
pca_cols2 = gps_data[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                     "accelerations","decelerations","percent_max_speed"
                     ]]

print('PCA')

gps_scaled = StandardScaler().fit_transform(pca_cols2)
pca = PCA(n_components=5)
pca_trnsfrm = pca.fit_transform(gps_scaled)

model_data = pd.DataFrame(pca_trnsfrm)
model_data.columns = ['PCA1','PCA2','PCA3','PCA4','PCA5']

# Several Possible Target Variables - Begin with predicting overuse injuries in the upcoming week
model_data['injury_flag'] = gps_data['overuse_injury_upcoming_week']

#Add in player variables and dates to include in reporting output
model_data[['player_id','player_name','overuse_injury_day','date']] = gps_data[['player_id','player_name','overuse_injury_day','date']]

print(model_data.head())

#################################################################################

# Load dataset
X = model_data.drop('injury_flag', axis=1)
y = model_data['injury_flag']

print('\nData Points that meet criteria for injury flag (within 1 week of an overuse injury)')
print(sum(y))

# Split dataset into training and testing sets
X_train_full, X_test_full, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

X_train = X_train_full.drop(['player_id','player_name','overuse_injury_day','date'],axis=1)
X_test = X_test_full.drop(['player_id','player_name','overuse_injury_day','date'],axis=1)

print('\nTotal Data Points (TEST)')
print(len(y_test))

print('\nData Points that meet criteria for injury flag (TEST)')
print(sum(y_test))

# Not Necessary since PCA was already performed
###################################################
# # Feature scaling
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

print('\nModel Output Injury Probabilities')
y_prob = model.predict_proba(X_test)

# Make predictions 
# Default of 50% threshold is too high, test various & get stakeholder feedback on sensitivity
if demo: 
    custom_threshold = 0.11
else:
    custom_threshold = 0.04
#y_pred = model.predict(X_test) - Uses 0.5 Threshold
y_pred = (y_prob[:,1] >= custom_threshold).astype(int)
print('\nData Points predicted to have injuries')
print(sum(y_pred))

# Evaluate the model
print('\nModel Results')
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred,zero_division=1))

#######################################################################

# Model Outputs, display results
print('\nModel Results Reporting')

# Join back in the results and plot the outputs
output_data_full = X_test_full
output_data_full['injury_prediction'] = y_pred
output_data_full['injury_predicted_prob'] = y_prob[:,1]
output_data_full['injury_flag'] = y_test

######################################
# Plotting Output Results
if demo:
    figures_prefix = 'figures/results/demo/'
else:
    figures_prefix = 'figures/results/actual/'

# Convert date to datetime, and sort appropriately
output_data_full['date'] = pd.to_datetime(output_data_full['date'])
output_data_full = output_data_full.sort_values('date')

output_data = output_data_full.groupby(['player_id','player_name','date','overuse_injury_day'],as_index=False).agg({'injury_predicted_prob':'mean','injury_prediction':'max','injury_flag':'max'})
from plotting import output_lineplot # type: ignore
from color_palette import player_colors, match_colors, position_colors #type: ignore

# (dataset,yvar,hue,plot_title,xlab,ylab,save_fig,fig_name,highlight_player,colors)
for player in output_data['player_name'].unique():
    print(f'\nPlottin results for: {player}')
    lname = player.split(' ',1)[1].lower().replace(' ','_')
    output_lineplot(output_data,'player_name','Trend of Injury Likelihood','Date','Injury Likelihood',True,f'{figures_prefix}results_injury_likelihood_{lname}.png',player,player_colors,custom_threshold)


####################################################################
# Save results to Data folder

print('\nSave Model Results to CSV')
model_results_file = data_dir / 'model_results.csv'
output_data.to_csv(model_results_file,index=False)


