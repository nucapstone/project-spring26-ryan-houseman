### Discussion of Plan for Project 
Updated: 3/24/2026

#### Overall Goals
The primary goal for this project is two-fold.  
1. Build a model that can effectively identify and flag players that are at an elevated risk for overuse injury and would benefit from additional rest/rehab.  
2. Deliver a process for refreshing data and regenerating results that is easy to run for the coaching staff, as well as front end reporting and data visualization highlighting model results.  Ideally, the coaching staff could download GPS data once or twice a week, 
have a push button process for running the model, and then have access to reporting results that are automatically refreshed.  The stakeholders could then use this information to help dictate and inform practice plans and player maintenance strategies.  This is especially 
important for players who have no current limitations imposed by athletic training staff, but may have a higher risk of incurring an injury.

#### V1 (First Half of Semester)
Now that I've access, cleaned, and prepped the data, the next order of business is to build the injury risk model.  I plan to use the next couple weeks to work on this development, and am hoping to explore the efficacy of a few different models.  
In general, one consideration that I'd like to test a bit is the decision on whether or not to model the data for players all together or to separate out for each player. 
One of the initial steps in this process (which will also help with reporting and visualizing results), is dimensionality reduction.  I plan to use PCA on the input data, and also plan to implement the T-SNE algorithm for data visualization.  

Logistic Regression
The first model I'd like to explore is logistic regression.  Given that the target variables of interest (could be a few of the injury flags), are indicator variables (1 for an injury, 0 for not), binary logistic regression makes sense as an approach for this model.
For any given data point, the output of this model would return a probability of an injury occurring for that player.  Depending on results, further discussion with the stakeholder may be required for flagging different probabilities/zones of risk in the output results.

Autoregressive Model (AR) 
In this model, the output variable depends on it's own previous values.  The thought here is that for each player, the entire collection of their data up to that point in the season could be used to help assess their current injury risk.  
The sklearn framework has an ARIMA (AutoRegressive Integrated Moving Average) model that could work well for this type of problem.

#### V2 (Updated 3/24/26)
The injury prediction logistic regression model described above has been fully implemented.  While there is some continued iteration and fine-tuning of this model, the results are satisfactory, and I've shifted my focus onto the data visualization and front-end reporting.  Possible implementation of an autoregressive model has been deprioritized because that would likely require me to train the model on each individual player's data, and would be difficult to refresh in upcoming seasons due to lack of timely access to the injury data.  My hope is that the athletic training staff can compile and share injury data at the completion of each season, and we can re-train the logistic regression model on the growing dataset.

For the front-end reporting, I'm leveraging many of the same tools and methods that we've learned thus far in CS5610.  After the model runs, I've developed a script to create a SQLite database with the model results.  I'm then using Flask to connect to this database and develop routes that will then be used to gather data for the front-end reporting and data visualizations.  I'm using Vite and React components on the front-end, and plan on building out 3 main pages (Team Overview, Player Overview, Player Detail).  Initial Implementations of Player Overview and Player Detail are complete, but I have several other features/plots/results I'd like to include, and need to do some work on the formatting and styling.  

My other focuses in the remaining weeks of the semester are to build out a process to refresh the data and model results.  I'm looking into whether this could be possible from the front-end itself.  It would be nice to have my stakeholders be able to refresh everything while only interacting with the webpage.  Either way, having as simple a process as possible for refreshing the data and reporting is a key focus.  

I also need to figure out how to host the web page (likely Github pages).  Currently the page is just being hosted locally.  

I'm working to schedule 2-3 more stakeholder meetings for the remainder of the semester.  I have plans to meet with stakeholders the week of 3/22.  Topics to discuss are...
* Reporting outputs & requests
* Web page styling
* Data & model refresh process
* Cadence for availability of future injury data and data requirements for model compatibility
* Logistic Regression model fine-tuning
