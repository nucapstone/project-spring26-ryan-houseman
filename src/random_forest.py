# Random Forest Model Implementation

####################################################################################################

from pathlib import Path
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.model_selection import (
    train_test_split, StratifiedKFold, RandomizedSearchCV
)
from sklearn.metrics import (
    roc_auc_score, brier_score_loss, log_loss,
    classification_report, RocCurveDisplay,
    precision_recall_curve, average_precision_score
)

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

import matplotlib.pyplot as plt
from scipy.stats import randint
from sklearn.model_selection import TimeSeriesSplit

#################################################################################
# Repository Folders
src = Path(__file__).resolve().parent
root = src.parent
data_dir_actual = root / 'data/actual'
data_dir_demo = root / 'data/demo'

#Check if there is any actual data to use, otherwise use the demo data
files = [f for f in os.listdir(data_dir_actual) if f.endswith(".csv")]
if files:
    data_dir = data_dir_actual
    demo=False
else:
    data_dir = data_dir_demo
    demo=True

#######################################
# # Test Demo Data
# data_dir = data_dir_demo
# demo=True

# Output directory for results
if demo:
    os.makedirs(root / "figures/results/demo/random_forest", exist_ok=True)

else:
    os.makedirs(root / "figures/results/actual/random_forest", exist_ok=True)

#################################################################################
# Upload Raw GPS Data
print('Upload Combined Dataset')
# Raw GPS Data
gps_data_file = data_dir / 'prepped_data.csv'
gps_data = pd.read_csv(gps_data_file)

#################################################################################
# GPS Columns for prediction Model
model_data = gps_data[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                     "accelerations","decelerations","percent_max_speed"
                     ]].copy()

# Several Possible Target Variables - Begin with predicting overuse injuries in the upcoming week
model_data['injury_flag'] = gps_data['overuse_injury_upcoming_week'].copy()

print(model_data.head())

#################################################################################
# Load dataset
X = model_data.drop('injury_flag', axis=1)
y = model_data['injury_flag']

########################################################################
X[['player_id','player_name','overuse_injury_day','date']] = gps_data[['player_id','player_name','overuse_injury_day','date']].copy()
X['date'] = pd.to_datetime(X['date'],format='%Y-%m-%d')

# Player ID is not included in model, so there is no need to split data based on a date cutoff
# Split Based on Dates to avoid leakage (i.e. The model is trained on a session from week 10, but then tested on a session from week 8 for the same player)
# cutoff_date = pd.Timestamp(X['date'].quantile(0.75))

# train_mask = X['date'] < cutoff_date
# test_mask  = X['date'] >= cutoff_date

# X_train_full = X[train_mask]
# X_test_full  = X[test_mask]
# y_train      = y[train_mask]
# y_test       = y[test_mask]

# Split dataset into training and testing sets
X_train_full, X_test_full, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

X_train = X_train_full.drop(['player_id','player_name','overuse_injury_day','date'],axis=1)
X_test = X_test_full.drop(['player_id','player_name','overuse_injury_day','date'],axis=1)

print(X_train.head())


# ############################################################################################################
# Hyperparameter search 
# Use StratifiedKFold so every fold preserves the minority class ratio.
# Score on ROC-AUC — better than accuracy for imbalanced problems.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=19)
cv = TimeSeriesSplit(n_splits=5)

param_dist = {
    "n_estimators":     randint(200, 600),
    "max_depth":        [None, 10, 20, 30],
    "min_samples_leaf": randint(5, 50),        # higher = smoother output probabilities
    "min_samples_split":randint(2, 20),
    "max_features":     ["sqrt", "log2", 0.3, 0.5],
    "class_weight":     ["balanced_subsample"],
    # balanced_subsample recomputes weights per bootstrap sample —
    # often better than global "balanced" for imbalanced data
}

base_rf = RandomForestClassifier(n_jobs=-1, random_state=42)

search = RandomizedSearchCV(
    estimator=base_rf,
    param_distributions=param_dist,
    n_iter=60,             # increase for a more thorough search (costs time)
    scoring="roc_auc",
    cv=cv,
    verbose=1,
    n_jobs=-1,
    random_state=42
)
search.fit(X_train, y_train)

print(f"\nBest CV ROC-AUC : {search.best_score_:.4f}")
print("Best params     :", search.best_params_)

####################################
#Best CV ROC-AUC : 0.7594
#Best params     : {'class_weight': 'balanced_subsample', 'max_depth': 20, 'max_features': 0.5,
#                    'min_samples_leaf': 20, 'min_samples_split': 2, 'n_estimators': 400}
#####################################

#################################################################################################################
# Calibrate the tuned model 
best_rf = search.best_estimator_

calibrated_rf = CalibratedClassifierCV(
    estimator=best_rf,
    method="sigmoid",    # swap to "sigmoid" for < ~1k training samples
    cv=5
)
calibrated_rf.fit(X_train, y_train)

#################################################################################################################
# Predict & build results table
probs = calibrated_rf.predict_proba(X_test)[:, 1]  

results = X_test.copy()
results["p_hat"] = probs
results["truth"] = y_test.values

print(results.head())

# Make predictions 
# Default of 50% threshold is too high, test various & get stakeholder feedback on sensitivity
# Recall vs Precision
# Better recall would correctly flag more injuries with less false positives
# Precision would miss more injuries, but have a higher overall accuracy 
#################################################################################################################
# Threshold tuning (precision / recall tradeoff) # Add to logistic regression!

precision, recall, thresholds = precision_recall_curve(y_test, probs)

# Option A — maximise F1 (balanced tradeoff)
f1 = 2 * precision * recall / (precision + recall + 1e-9)
best_f1_idx = np.argmax(f1)
thresh_f1   = thresholds[best_f1_idx]

# Option B — target a minimum recall (e.g. catch ≥80% of positives)
MIN_RECALL  = 0.50
viable      = thresholds[recall[:-1] >= MIN_RECALL]
thresh_r50  = viable[-1] if len(viable) else thresholds[best_f1_idx]

print(f"\n── Threshold options ────────────────────────────────────")
print(f"\n── Threshold options ────────────────────────────────────")
print(f"  Max-F1 threshold   : {thresh_f1:.3f}")
print(f"  ≥50% recall thresh : {thresh_r50:.3f}")

# Choose which threshold to apply (swap to thresh_r80 if recall matters more)
THRESHOLD = thresh_r50
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
    figures_prefix = 'figures/results/demo/random_forest/'
else:
    figures_prefix = 'figures/results/actual/random_forest/'

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
plt.savefig(f"{figures_prefix}rf_imbalanced_eval.png", dpi=150)

#####################################################################################################
# Feature importance 
# best_estimator_ is a single fitted RF, so .feature_importances_ is direct
feat_imp = (
    pd.Series(best_rf.feature_importances_, index=X_train.columns)
    .sort_values(ascending=False)
    .head(10)
)
print("\n── Top 10 Feature Importances ───────────────────────────")
print(feat_imp.to_string())

######################################################################################################
# Run the model on the Current Season Data
print('################################################')
print('Part 2: \n################################################')
print('\nUpload Current Season Data - Run Model')

gps_data_file_c = data_dir / 'prepped_data_current.csv'
gps_data_c = pd.read_csv(gps_data_file_c)


#################################################################################
# GPS Columns for prediction Model - Current Season
model_data_c = gps_data_c[["duration","load","distance","yards_per_minute","high_intensity_yards","high_intensity_events","sprint_distance","sprints","top_speed","avg_speed",
                     "accelerations","decelerations","percent_max_speed","player_id","player_name","date"
                     ]].copy()

#################################################################################

# Load dataset
X_cur = model_data_c.drop(['player_id','player_name','date'],axis=1)

# Current Season Predicted Probabilities
print('\nCurrent Season Output Injury Probabilities')
probs = calibrated_rf.predict_proba(X_cur)[:, 1]  

# Current Season Reporting
print('\nReporting Current Season')

# Join back in the results and plot the outputs
model_out_full = model_data_c
model_out_full['injury_prediction'] = results["pred"]
model_out_full['injury_predicted_prob'] = probs

######################################################################################################
# # Save results to Data folder
print('\nSave Model Results to CSV - Current Season')
model_results_file = data_dir / 'model_results_rf.csv'
model_out_full.to_csv(model_results_file,index=False)



