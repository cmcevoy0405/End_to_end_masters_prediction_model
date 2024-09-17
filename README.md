<h1 align="center" style="color:#FFFFFF; font-family: 'Arial', sans-serif;">Masters Prediction Project ⛳</h1> <p align="left" style="color:#FFFFFF; font-family: 'Verdana', sans-serif;"> <b>Key Findings: It seems that players who finished well in the tournament performed strongly from tee to green and off the tee, as well as scoring well throughout the year and gaining a high number of strokes. On the other hand, putting and driving distance seemed to affect Masters performance the least. The final classification model was able to predict the winner among a group of winners correctly 86% of the time.</b> </p>

### Table of Contents
- [Business problem](#business-problem)
- [Introduction](#introduction)
- [Scraping](#scraping)
- [Model](#model)
- [Deployment](#deployment)
- [Limitations](#limitations)

### Business Problem
Golf is one of the biggest sports in the world in 2024, with over 450 million fans. This project covers two topics of interest: it can be used to predict the odds of a player winning the tournament, thereby allowing betting agencies to set odds. The Flask application also allows golf fanatics to interact and compare themselves with the world's best, showing them how likely they are to win the Masters.

### Introduction
I've always been interested in golf and what makes the best in the world the best. Combined with my interest in data and finding data-backed solutions, I decided to create a model to predict who would win the Major golf tournament, the Masters. This involved the full data process from web scraping and model building through to deployment. The entire project was developed in Python using Flask as the deployment method.

### Scraping
The pga_scrape.py file showcases the data scraped from a Python script. The file scrapes the last 15 years' worth of PGA data on players who competed in the 2024 Masters tournament. I extracted 18 variables for analysis:
 
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


It is important to note that this treats each player as a different data point for every year; for example, there would be 15 data points for Rory McIlroy, one for every year.

I combined all these variables into one final dataframe, discarding all players who were not competing in the 2024 Masters.

### Model

#### Data cleaning
Some basic data cleaning was conducted, stripping 'T's off tied positions and converting the necessary columns to numeric. I specifically imputed one missing value into the 2018 Masters winner, thus adding one more data point of the minority class. Any other missing values were dropped. All variables were assessed for normal distribution, leading to top 10 finishes and 1st place finishes being dropped due to skewness.

### Exploratory Analysis
I created a boolean column identifying whether or not the player finished in the top 10 in the Masters that year. Additionally, I separated my predictor variables from my dataframe, distinguishing Masters winners and top 10 finishers from the rest of the field for visualization.

I then created a boxplot for each predictor variable comparing top 10 finishers to the rest of the field and similarly for Masters winners. This showed that average score, total strokes gained, strokes gained tee to green, and strokes gained off the tee are vital predictors for success in the Masters. On the other hand, putting and driving distance proved to be less important features for Masters winners.

#### Predictor feature importance
- 0 Avg_score	0.253433
- 1	Drive Avg	0.029653
- 2	%_of_fairways_hit	0.064524
- 3	Putts per round	0.033271
- 4	GIR %	0.047483
- 5	Scramble %	0.023129
- 6	Bounce_Back %	0.050745
- 7	Total Strokes Gained	0.127927
- 8	SG:OTT	0.072963
- 9	SG:ARG	0.063059
- 10	SG:TTG	0.085042
- 11	SG:APG	0.030276
- 12	SG:PUTT	0.026004
- 13	Par 3 Score	0.022345
- 14	Par 4 score	0.053538
- 15	Par 5 score	0.016610

#### Model Building
Due to the large class imbalance, I employed SMOTE and random undersampling to both create fictional winners based on the nearest data point and randomly remove samples from the dataframe. I chose to measure this model on precision, recall, and F1 score, with particular attention to recall, as I wanted a high chance of picking a winner even if it meant there was a higher chance of a loser being chosen as well.

I first ran the model trying to predict top 10 positions, which produced a decent recall of 0.71. I then tested different classification models, one using RandomForestClassifier and the other two using a Support Vector Classifier. The Support Vector Classifier with a linear kernel performed the best. With hyperparameters optimized, the final model produced a recall of 0.61 on the testing data.

#### Model Results
I ran the final model 1000 times to gain an accurate assessment of the model's performance. As I was trying to predict the 2024 Masters, which had already taken place, I knew the winner. This was purposefully done to measure the model's performance on unseen data. The actual winner appeared in a winners list 838 times out of a thousand, showing that there is some merit to this model.

### Deployment
This was my first time deploying a model, so I took a simple approach by designing an HTML web page and a Flask application to interact with the two pages.

- index.html allows a user to input they're golf statistics (or anybody they wish).
- app.py is a flask application that takes the users input from the index.html file and runs it through the trained model in the backend.
- results.html displays the percentgae chance that the player will win the masters tournament.

This allows real-time data to be fed into the model and immediate results to be obtained.

### Limitations
This project isn't without its limitations and issues. Firstly, the web scraper could be improved; it is a large amount of repeatable code that could be more dynamic by running more for loops through it. However, I couldn't get that approach to work, so I settled for scraping each variable one at a time.

Secondly, a lot of years' winners were missing significant amounts of data, so they had to be dropped. Imputation or further research could prove beneficial to the model's accuracy, but for only a few years, this did not seem worth the effort.

Lastly, the Flask application is rather basic, and it is highly unlikely an amateur golfer has all these variables recorded. However, I could add an option to select from top PGA players and retrieve the likelihood they'll win the upcoming Masters.



