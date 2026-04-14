# Logistic Regression Model Implementation

###########################################################################
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import (
    roc_auc_score, brier_score_loss, log_loss,
    classification_report, RocCurveDisplay,
    precision_recall_curve, average_precision_score
)
from sklearn.calibration import calibration_curve
import os

import seaborn as sns
import matplotlib.pyplot as plt
from plotting import output_lineplot # type: ignore
from color_palette import player_colors, match_colors, position_colors #type: ignore


#################################################################################
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

#######################################
# Test Demo Data
# data_dir = data_dir_demo
# demo=True

#######################################

# Output directory for results
if demo:
    os.makedirs(root / "figures/results/demo/logistic_regression", exist_ok=True)

else:
    os.makedirs(root / "figures/results/actual/logistic_regression", exist_ok=True)

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
pca = PCA(n_components=8)
pca_trnsfrm = pca.fit_transform(gps_scaled)

model_data = pd.DataFrame(pca_trnsfrm)
model_data.columns = ['PCA1','PCA2','PCA3','PCA4','PCA5','PCA6','PCA7','PCA8']

# Model Target Variable - Overuse injuries in upcoming window of time (7 days or 10 days)
target_variable = 'overuse_injury_upcoming_week'
prediction_window = 7
model_data['injury_flag'] = gps_data[target_variable]

#Add in player variables and dates to include in reporting output
model_data[['player_id','player_name','overuse_injury_day','date','distance','top_speed','percent_max_speed']] = gps_data[['player_id','player_name','overuse_injury_day','date','distance','top_speed','percent_max_speed']]

print(model_data.head())

#################################################################################

# Load dataset
X = model_data.drop('injury_flag', axis=1)
y = model_data['injury_flag']

print(f'\nData Points that meet criteria for injury flag (within {prediction_window} days of an overuse injury)')
print(sum(y))

# Split dataset into training and testing sets
X_train_full, X_test_full, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

X_train = X_train_full.drop(['player_id','player_name','overuse_injury_day','date','distance','top_speed','percent_max_speed'],axis=1)
X_test = X_test_full.drop(['player_id','player_name','overuse_injury_day','date','distance','top_speed','percent_max_speed'],axis=1)

print('\nTotal Data Points (TEST)')
print(len(y_test))

print('\nData Points that meet criteria for injury flag (TEST)')
print(sum(y_test))

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

print('\nModel Output Injury Probabilities')
probs = model.predict_proba(X_test)[:, 1]

# Make predictions 
# Default of 50% threshold is too high, test various & get stakeholder feedback on sensitivity
# Recall vs Precision
# Better recall would correctly flag more injuries with less false positives
# Precision would miss more injuries, but have a higher overall accuracy 

#################################################################################################################
# Threshold tuning (precision / recall tradeoff)

results = X_test.copy()
precision, recall, thresholds = precision_recall_curve(y_test, probs)

# Option A — maximise F1 (balanced tradeoff)
f1 = 2 * precision * recall / (precision + recall + 1e-9)
best_f1_idx = np.argmax(f1)
thresh_f1   = thresholds[best_f1_idx]

# Option B — target a minimum recall
if demo:
    MIN_RECALL = 0.30
else:
    MIN_RECALL  = 0.50
viable      = thresholds[recall[:-1] >= MIN_RECALL]
thresh_recall  = viable[-1] if len(viable) else thresholds[best_f1_idx]

print(f"\n── Threshold options ────────────────────────────────────")
print(f"  Max-F1 threshold   : {thresh_f1:.3f}")
print(f"  ≥50% recall thresh : {thresh_recall:.3f}")

THRESHOLD = thresh_recall
results["pred"] = (probs >= THRESHOLD).astype(int)

print(results.head())

#################################################################################################################
# Evaluate 
print(f"\n── Performance (threshold = {THRESHOLD:.3f}) ────────────────")
print(f"  ROC-AUC      : {roc_auc_score(y_test, probs):.4f}")
print(f"  Avg precision: {average_precision_score(y_test, probs):.4f}  "
      f"(PR-AUC — better metric for imbalanced data)")
print(f"  Brier score  : {brier_score_loss(y_test, probs):.4f}")
print(f"  Log-loss     : {log_loss(y_test, probs):.4f}")
print("\n── Classification Report ────────────────────────────────")
print(classification_report(y_test, results["pred"],
                             target_names=["class 0", "class 1"]))

#################################################################################################################
# Plots
if demo:
    figures_prefix = 'figures/results/demo/logistic_regression/'
else:
    figures_prefix = 'figures/results/actual/logistic_regression/'

fig, axes = plt.subplots(1, 3, figsize=(17, 5))

# A — Reliability diagram
frac_pos, mean_pred = calibration_curve(y_test, probs, n_bins=10)
axes[0].plot([0,1],[0,1], "k--", label="Perfect")
axes[0].plot(mean_pred, frac_pos, "o-", color="steelblue", label="Calibrated RF")
axes[0].set(xlabel="Mean predicted prob", ylabel="Fraction positives",
            title="Reliability diagram")
axes[0].legend()

# B — Precision-Recall curve (more informative than ROC for imbalanced data)
axes[1].plot(recall, precision, color="darkorange")
axes[1].axvline(recall[best_f1_idx], color="steelblue",
                linestyle="--", label=f"Max-F1 @ R={recall[best_f1_idx]:.2f}")
axes[1].set(xlabel="Recall", ylabel="Precision", title="Precision-Recall curve")
axes[1].legend()

# C — ROC curve
RocCurveDisplay.from_predictions(y_test, probs, ax=axes[2], name="Calibrated RF")
axes[2].set_title("ROC curve")

plt.tight_layout()
plt.savefig(f"{figures_prefix}lreg_evaluation.png", dpi=150)

######################################################################################################

# Model Outputs, display results
print('\nModel Results Reporting')

# Join back in the results and plot the outputs
output_data_full = X_test_full
output_data_full['injury_prediction'] = results["pred"]
output_data_full['injury_predicted_prob'] = probs
output_data_full['injury_flag'] = y_test

######################################################################################################
# Plotting Output Results
if demo:
    figures_prefix = 'figures/results/demo/logistic_regression/'
else:
    figures_prefix = 'figures/results/actual/logistic_regression/'

# Convert date to datetime, and sort appropriately
output_data_full['date'] = pd.to_datetime(output_data_full['date'])
output_data_full = output_data_full.sort_values('date')

output_data = output_data_full.groupby(['player_id','player_name','date','overuse_injury_day'],as_index=False).agg({'injury_predicted_prob':'mean','injury_prediction':'max','injury_flag':'max'})

for player in output_data['player_name'].unique():
    lname = player.split(' ',1)[1].lower().replace(' ','_')
    output_lineplot(output_data,'player_name','Trend of Injury Likelihood','Date','Injury Likelihood',True,f'{figures_prefix}results_injury_likelihood_{lname}.png',player,player_colors,THRESHOLD,prediction_window)


######################################################################################################
# Run the model on the Current Season Data
print('################################################')
print('Part 2: \n################################################')
print('\nUpload Current Season Data - Run Model')

gps_data_file_c = data_dir / 'prepped_data_current.csv'
gps_data_c = pd.read_csv(gps_data_file_c)


#################################################################################
# Run PCA on GPS Data
pca_cols2_c = gps_data_c[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                     "accelerations","decelerations","percent_max_speed"
                     ]]


gps_scaled_c = StandardScaler().fit_transform(pca_cols2_c)
pca = PCA(n_components=8)
pca_trnsfrm_c = pca.fit_transform(gps_scaled_c)

model_data_c = pd.DataFrame(pca_trnsfrm_c)
model_data_c.columns = ['PCA1','PCA2','PCA3','PCA4','PCA5','PCA6','PCA7','PCA8']

#Add in player variables and dates to include in reporting output
model_data_c[['player_id','player_name','date','distance','top_speed','percent_max_speed']] = gps_data_c[['player_id','player_name','date','distance','top_speed','percent_max_speed']]

#################################################################################

# Load dataset
X_cur = model_data_c.drop(['player_id','player_name','date','distance','top_speed','percent_max_speed'],axis=1)

# Current Season Predicted Probabilities
print('\nCurrent Season Output Injury Probabilities')
probs = model.predict_proba(X_cur)[:, 1]

# Current Season Reporting
print('\nReporting Current Season')

# Join back in the results and plot the outputs
# Consider Re-tuning Threshold?
model_out_full = model_data_c
model_out_full['injury_prediction'] = (probs >= THRESHOLD).astype(int)
model_out_full['injury_predicted_prob'] = probs
model_out_full['prediction_threshold'] = THRESHOLD
model_out_full['prediction_window'] = prediction_window

######################################################################################################
# # Save results to Data folder
print('\nSave Model Results to CSV - Current Season')
model_results_file = data_dir / 'model_results_lreg.csv'
model_out_full.to_csv(model_results_file,index=False)


