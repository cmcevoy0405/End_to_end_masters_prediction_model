Masters Prediction project

Overview:
This project entails a full end to end data science project that involves data scraping, model training and the creation of an API and html based website that interacts with real time data.

PGA_SCRAPE.PY
The pga_scrape file uses a graphql API to interact with the official PGA website and has scraped the last 15 years of data for all players on the PGA tour.
The data scraped inludes all participants in the 2024 masters tournament. 

Predcitor variables gathered include:
-Avergae Score
-Driving distance
-Top 10 finishes
-1st place finishes
-Percentage of fairways hit
-scramble percentage
-Bounce back percentage
-Putts per round
-Greens in regulation percentage
-Total strokes gained
-stroked gained off the tee
-Strokes gained tee to green
-Strokes gained approach to green
-Strokes gained around the green
-Strokes gained putting
-Par 3 average score
-Par 4 average score
-Par 5 average score

The target variable scraped was masters finish for each year.
The scraping method i choose could be improved apon by creating a series of for loops, however this method worked perfect for me and was easy to implement.

The final Dataframe created involved a concatenaton of all variables which was subsequently merged with the dataframe containing all participants for the upcoming masters.
Thererfore striping all players that were not of interest.

MASTERS_PREDICTION_MODEL


