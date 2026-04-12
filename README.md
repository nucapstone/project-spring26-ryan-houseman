# Roux Institute Spring 2026 - Data Science Capstone Project
## Ryan Houseman

Project Name: GPS Driven Overuse Injury Prediction Model

Team Lead: Ryan Houseman

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Stakeholders
* Bowdoin Soccer Coaching Staff: Scott Wiercinski & Andrew Banadda

## Background
* In the Fall 2025 Season, the Bowdoin College soccer team began using a GPS tracking sevice through PlayerData to collect GPS data on player movement for practices and games.  Many other collegiate teams across many sports are beginning to do the same.  The service provides some reporting on this data, but at the college level, small coaching staffs often don't have the resources or time to do their own in depth analysis.  The purpose of this project is to leverage the GPS data from PlayerData to build a player injury prediction model and develop a front-end with reporting from the model outputs.
 
## Data
* GPS player tracking (from PlayerData https://playerdata.com/en-us)
    * Includes various quantitative metrics on speed, distance, acceleration/deceleration
    * Categorical values related to player position, and training session/match information
    * Fall 2025 data includes ~5000 records of of player data for 28 players over the course of the season.  Data is available in CSV format.
    * The GPS data is easily downloaded from PlayerData's portal using the CSV Builder tool.  Include all available columns in the raw data, and use yards as the default distance. 
*  Injury report data available in CSV format detailing player injuries throughout the Fall 2025 season.

GPS and Injury data for the Fall 2025 season is used to build and train the overuse injury prediction model.  Throughout the upcoming Fall 2026 season, the Bowdoin coaching staff, can regularly apply the model to current GPS data.  At the completion of each season, injury data can be compiled and appended to the training data.  Yearly updates to the training data are expected to help improve model performance over time.  

In order to maintain the privacy of the Bowdoin Soccer GPS and Injury data, DEMO datasets have been created and are the only data available in this repository.  DEMO data inputs are listed below.  If you wish to run this model on your own PlayerData output and Injury data, you will need to populate data/actual/ with csv files of the same format as the DEMO files listed below.  The model scripts will automatically use any data placed in data/actual/ but will otherwise use the DEMO data files. 

Input DEMO data files:
Model Training Data
* data/demo/gps_data_raw_model.csv
* data/demo/injury_data_raw.csv

GPS Data from Current Season
* data/demo/gps_data_raw_current.csv

## Model Overview
The implementation of this project includes both a logistic regression model and a random forest model used to predict the likelihood of an overuse injury occurring in during an upcoming window of time.  The model currently uses a 7 day window for injury predictions, and 10 days was also tested with similar results.  For both models, the model is trained using cross-validation on all available training data, and then run on the current season's data for front-end reporting.    

### Logistic Regression
For the logistic regression model, only numerical values in the GPS data are used as inputs.  Principal Component Analysis is performed to help standardize data and handle correlation that became evident during the exploratory analysis early on in this project.  The possibility of using one-hot encoded variables for categorical data was tested, but this rendered the numerical data less important.  There were also concerns that including categorical data could make the model less broadly useful for future seasons or different teams.  There was also testing done to determine how many principal components should be used as model inputs, 8 are currently used.       

### Random Forest
The random forest model uses the same numerical inputs as the logistic regression model, but PCA is not performed and each of the columns are used directly within the model.  There are more input parameters used for a random forest implementation and hyperparameter search is used to help determine the best subset of for the model.  Random forests also average model outputs to assign injury likelihoods for each data point, which can result in inaccurate probabilities.  Because of this, a sigmoid calibration is also applied to the model to improve likelihood outputs.    

## Model Results
Due to the significant class imbalance in the model's target variable (occurrence of an overuse injury in the upcoming week), using model accuracy alone is insufficient to judge model performance.  Additionally, because of the purpose of the model is to flag players at elevated risk for overuse injury, it's important that metrics focus on correctly predicting injuries.  Precision-Recall Curves, ROC curves, and Brier scores were primarily used to gauge model efficacy.  Neither model achieved earth-shattering results, but the logistic model performs reasonably well across these metrics. Despite some early promise, the random forest model was relatively ineffective.  Because of this, logistic regression is currently set as the default option for front-end reporting.  There is reason to believe both models could improve as more data becomes available over time.

Logistic Regression results:
* ROC-AUC score: 0.725
* Average Precision: 0.106
* Brier score: 0.038
  
<img width="950" height="417" alt="image" src="https://github.com/user-attachments/assets/ebf846ac-1588-4828-8ff0-a634a5efa8c8" />

Average precision is typically considered one of the best ways to gauge model performance when a class imbalance is present, because it focuses on the correct prediction of injuries.  It's impacted by two factors:
* Precision - of all the datapoints flagged for injury, how often was this correct (i.e. how many of those players actually sustained an overuse injury within the next week)
* Recall - of all the actual overuse injuries, how often does the model flag them

Although the average precision score for the model isn't great, there's a reasonable explanation for this.  Within a week of an injury, a player may have 7 or more data points available.  As dictated by the model configurations, each of those data points are a 1.  In reality, it's not expected that the signs of an overuse injury would be present in all of those data points (some practices may be easier, so it's hard to tell if a player is seriously fatigued or susceptible to injury).  Because of this, the reporting associated with the model outputs focuses on a higher recall and identifying players who have multiple flags within a short timespan.  While some players may be incorrectly flagged for injury, most injuries do have several data points flagged within a 7 day window leading up to the injury.          

## Reporting Overview
Alongside the injury prediction model, the goal of this project is to provide easily refreshable front-end reporting of the model results.  This allows for quick indentification of players who are at risk for overuse injury, and a coaching staff can update training or recovery plans accordingly.  This front-end is implemented in Vite using React components, and the DEMO version of this model and reporting is published through Github Pages.

INCLUDE LINK TO REPORTING HERE!

** Add documentation for how to launch the BMS Injury Prediction Webpage (NEED A NAME FOR THIS!)

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Running the Code & Reproducability
Below is the current guidance for running the various components of this data pipeline and front-end output.  Future work on the project may include the implementation of a backend, which could allow users to refresh the model and reporting while only interactive with the front-end.     

#### Required Software
The code for this project was written and run using a Conda environment for software and package management.  Please follow instructions in [conda.md](https://github.com/ds5110/git-intro/blob/main/conda.md) for more guidance on setting up a Conda environment.  

All software required for running the code is located in [environment.yml](environment.yml).  Please setup your environment with all software and packages included in that file. 

Additionally, Node.js is used for some of the front-end reporting.  This is installed outside of Conda, please follow the instructions in [node.md](https://github.com/ds5110/git-intro/blob/main/node.md) for guidance on installing Node.js.  This also requires a user

#### Makefile
The repository has a Makefile available to allow a user to easily step through the data pipeline for this project.  Please run the following make commands in order to reproduce the predictive model and reporting.  Some additional make commands for EDA, dimensionality reduction, and the random forest model are also available.   

```
make demo_data     #This command runs the src/demo_setup.py file which creates a demo dataset.  If actual data is stored in the appropriate folder, the data pipeline will use the real data and this command is not necessary.  

make data_prep     #This command runs the src/data_prep.py file which joins and cleans the 2 input data files and produces data/bms_data_2026.csv

make model_lreg    #This command runs src/logistic_regression.py which runs the logistic regression model, outputs plots to figures/results/ and creates data/model_results.csv

make rpt_data      #This command runs reporting/rpt_data_setup.py which generates JSON output files used for the front-end reporting

make dev_setup     #This command runs the npm install command, which is required for the front-end reporting.  This only needs to be run once.  

make run_dev       #This command uses npm to launch the front-end output of the project
```

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

