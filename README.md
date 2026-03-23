# DS5500 Spring 2026 - Data Science Capstone Project
## Ryan Houseman

Project Short Name: soccer

Project Name: Bowdoin Soccer GPS Player Tracking - Injury Risk Analysis

Team Lead: Ryan Houseman

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Stakeholders
* Bowdoin Soccer Coaching Staff: Scott Wiercinski (swiercin@bowdoin.edu) & Andrew Banadda (a.banadda@bowdoin.edu)

Story
* In the Fall 2025 Season, the Bowdoin College soccer team began wearing GPS tracking devices for all of their practices and games.  Many other collegiate teams across many sports are beginning to do the same thing.  The service the Bowdoin team uses provides some high level reports on this data, but at the college level, coaches often don't have the resources/ability to do their own in depth analysis.  The Bowdoin Men's Soccer coaching staff is hoping to use the GPS tracking data to build a model and reporting on player injury risk.  
 
* For each player, the GPS device tracks their position on the field throughout a training session or match.  As part of this, a number of other metrics are gethered such as distance run, # of sprints, time spent sprinting, accelerations, etc.  Given the high physical workload, muscular injuries related to overuse are very common in college soccer.  My plan is to use this data to build a model predicting when players begin to show signs of fatigue and overuse.  The coaching staff could then use these results to help manage player workloads and hopefully prevent more serious injuries.  
 
* There's a lot of room for different ML work on this data, but I think there's also a good use case for some sort of front end reporting/data visualization.

Data
* GPS player tracking data results
    * Includes various quantitative metrics on speed, distance, acceleration/deceleration
    * Categorical values related to player position, and training session/match information
    * Data includes ~5000 records of of player data for 28 players over the course of the fall season.  Data is available in CSV format. 
*  Injury report data available in CSV format detailing plaeyer injuries throughout the fall season
