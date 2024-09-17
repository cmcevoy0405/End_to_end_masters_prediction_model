<h1 align="center" style="color:#FFFFFF; font-family: 'Arial', sans-serif;">Masters Prediction Project ⛳</h1>

<p align="left" style="color:#FFFFFF; font-family: 'Verdana', sans-serif;">
  <b>Key Findings: It seems that players who finished well in the tournament played well from tee to green, with driving distance and accuracy showing high importance. On the other hand putting and around the green play seemed to effect masters performance the least. The end calssification model was able to predit the winner among a winners group corrrectly 86% of the time.  </b>
</p>

### Table of Contents
- [Introduction](#introduction)
- [Scraping](#scraping)
- [Model](#model)
- [Deployment](#deployment)
- [Issues](#issues)

### Introduction
I've always been interested in golf and what makes the best in the world the best. Combined with my interest in data and finding data backed solutions, i decided to create a model on who would win the Major golf tournament, the masters.  This involved the full data process from web scraping and model building through to deployment. The entire project was developed in python using flask application as the deployment method. 

### Scraping
The pga_scrape.py file showcases the data scraped from a python script. The file scrapes the last 15 years worth of pga data on players that competed in the 2024 masters tournament. I extracted 18 variables for analysis:
 
- Driving Distance
- Top 10 finishes
- 1st position finishes
- Average score
- Percentage of fairways hit
- Putts Per round
- Percentage of Greens in regulation
- Scramble Percentage (The players ability to make par from a missed green in regulation)
- Total Strokes gained
- Strokes gained: Off the tee
- Strokes gained: Around the green
- Strokes gained: Tee to green
- Strokes gained: Approach to the green
- Strokes gained: Putting
- Par 3 score
- Par 4 score
- Par 5 score
- Master's finish (Predictor Variable)


It is important to note that this treats each player as a different data point for every year for example there would be 15 data points for Rory McIlroy, one for every year.

I combined all these varaibles in one final dataframe, discarding all players that were not competing in the 2024 masters.

### Model

#### Data cleaning
Some basic data cleaning was conducted, striping T's off tied positions and converting the necessary columns to numeric. I specifically imputed one missing values into the 2018 masters winner therfore giving one more data point of the minority class. Any other mising values were dropped.

#### Exploartory Analysis

I created a boolean type column identifying weather or not the player finished in the top 10 in the masters that year. Additonally I seperated my predcitor variables from my dataframe, seperated masters winners and top 10 finishers from the rest of the field for visualisation.

I then created a boxplot for each predictor variable comparing top 10 finishers to the rest of the field and similarily for masters winners. 


