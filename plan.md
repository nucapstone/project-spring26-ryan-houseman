### Discussion of Plan for Project

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

#### V2 (Second Half of Semester)
Once I have the initial framework of the models built, I plan orient my focus on effectively reporting model results.  Of course, I will continue to fine-tune the models throughout the semester, and will be looking for opportunities to improve on the initial results. 
For my stakeholders, it's important that refreshing the model on the latest GPS data and interpreting model results is easy to do.  I'd like to build some sort of front end output that can be used to host and automatically refresh results and visualizations.  
