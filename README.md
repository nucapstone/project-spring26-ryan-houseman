# DS5500 Spring 2026 - Data Science Capstone Project
## Ryan Houseman

Project Short Name: bowdoin_soccer

Project Name: Bowdoin Soccer GPS Player Tracking - Injury Risk Analysis

Team Lead: Ryan Houseman

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Stakeholders
* Bowdoin Soccer Coaching Staff: Scott Wiercinski (swiercin@bowdoin.edu) & Andrew Banadda (a.banadda@bowdoin.edu)

## Background
* In the Fall 2025 Season, the Bowdoin College soccer team began wearing GPS tracking devices for all of their practices and games.  Many other collegiate teams across many sports are beginning to do the same.  The service the Bowdoin team uses provides some high level reports on this data, but at the college level, coaches often don't have the resources/ability to do their own in depth analysis.  The purpose of this project is to leverage the Bowdoin Soccer GPS data to build a player injury prediction model, and provide the coaching staff with reporting from the model outputs.
 
## Data
* GPS player tracking (from PlayerData)
    * Includes various quantitative metrics on speed, distance, acceleration/deceleration
    * Categorical values related to player position, and training session/match information
    * Fall 2025 data includes ~5000 records of of player data for 28 players over the course of the season.  Data is available in CSV format. 
*  Injury report data available in CSV format detailing player injuries throughout the Fall 2025.

The intention of this project is to use the Fall 2025 data to build out the initial prediction model and reporting.  Once productionalized, GPS data could be refreshed regularly and run through the model to see timely predictions & player updates. Injury data will likely be refreshed once a season.

Input data files:
* data/gps_data_raw.csv
* data/injury_data_raw.csv

## Model Overview
The implementation of this project uses a Logistic Regression model to predict the likelihood of an overuse injury occurring in the upcoming week.  The inputs for this model are currently the 5 principal components of the GPS output's numerical data obtained through Principal Component Analysis (PCA).  It would be possible to include One-hot encoded variables for categorical variables (such as player name or position), but this renders the numerical data less important.  Given that the roster will continue to evolve every year, I've decided to focus on only the numerical outputs of the GPS data.  Further model testing and tuning will continue throughout the project, and conversations with stakeholders have provided valuable guidance on model assumptions and configuration.

** Add a Data Pipeline Markdown & Results & Analysis Markdown for more detailed discussion

## Reporting Overview
Alongside the injury prediction model, the goal of this project is to provide easily refreshable front-end reporting of the model results.  This will allow the Bowdoin soccer coaching staff to quickly indentify players who are at risk of overuse injury, and update training and recovery plans accordingly.  The back-end of this reporting will be implemented using Flask, and the front-end of the reporting will be implemented in Vite using React components.  This work is currently in developoment, but the intention is to have the following pages that highlight various aspects of current model results.

* Team Overview
* Player Overview
* Player Detail

** Add documentation for how to launch the BMS Injury Prediction Webpage (NEED A NAME FOR THIS!)


-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Running the Code & Reproducability
One of the focuses of my project is to identify a way for the Bowdoin College coaching staff to easily refresh model results and reporting.  Research for this underway, and I hope to simplify this is much as possible by the end of the semester.  As it stands, here is the current guidance for running the various components of this data pipeline and front-end output.   

#### Required Software
The code for this project was written and run using a Conda environment for software and package management.  Please follow instructions in [conda.md](https://github.com/ds5110/git-intro/blob/main/conda.md) for more guidance on setting up a Conda environment.  

All software required for running the code is located in [environment.yml](environment.yml).  Please setup your environment with all software and packages included in that file. 

Additionally, Node.js is used for some of the front-end reporting.  This is installed outside of Conda, please follow the instructions in [node.md](https://github.com/ds5110/git-intro/blob/main/node.md) for guidance on installing Node.js.

#### Makefile
The repository has a Makefile available to allow a user to easily step through the data pipeline for this project.  Please run the following make commands in order to reproduce the predictive model and reporting. 

```
make demo_data    #This command runs the src/demo_setup.py file which creates a demo dataset.  If actual data is stored in the appropriate folder, the data pipeline will use the demo data.  

make data_prep    #This command runs the src/data_prep.py file which joins and cleans the 2 input data files and produces data/bms_data_2026.csv

make model    #This command runs src/logistic_regression.py which runs the logistic regression model, outputs plots to figures/results/ and creates data/model_results.csv

make rpt_data    #This command runs reporting/rpt_data_setup.py which generates JSON output files used for the front-end reporting

# NOTE: If npm is not installed, you'll need to run npm install within the reporting/client/ directory of this repository before running the following commmand.
make run_dev    #This command uses npm to launch the front-end output of the project
```

As the semester concludes, I am working out the best & simplest approaches to refresh the model and results as well as figuring out how to host the front-end output (likely Github pages).  The documentation and guidance here will be updated to reflect any of these advancements in the coming weeks. 





