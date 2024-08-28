Masters Prediction Project
Overview:

This project entails a full end-to-end data science workflow that involves data scraping, model training, and the creation of a Flask application and HTML-based website that interacts with real-time data.

pga_scrape.py
The pga_scrape.py file uses a GraphQL API to interact with the official PGA website and has scraped the last 15 years of data for all players on the PGA Tour. The data scraped includes all participants in the 2024 Masters Tournament.

Predictor variables gathered include:

Average Score
Driving Distance
Top 10 Finishes
1st Place Finishes
Percentage of Fairways Hit
Scramble Percentage
Bounce Back Percentage
Putts Per Round
Greens in Regulation Percentage
Total Strokes Gained
Strokes Gained Off the Tee
Strokes Gained Tee to Green
Strokes Gained Approach to Green
Strokes Gained Around the Green
Strokes Gained Putting
Par 3 Average Score
Par 4 Average Score
Par 5 Average Score
The target variable scraped was the Masters Finish for each year. The scraping method I chose could be improved by creating a series of loops; however, this method worked perfectly for me and was easy to implement.

The final DataFrame created involved a concatenation of all variables, which was subsequently merged with the DataFrame containing all participants for the upcoming Masters, thereby filtering out all players that were not of interest.

masters_prediction_model.py
The masters_prediction_model.py file contains the code used to train the model. Initially, I separated the DataFrame into the training data (all years prior to 2024) and the testing data (the year 2024).

Data cleaning involved converting all necessary columns to numeric and handling string values. Two new columns were feature-engineered: one binary column indicating whether a player finished in the top 10 in the Masters, and the second column indicating if the player won the Masters.

All data was plotted on a histogram to assess normal distribution. The top_10_finishes and 1st_place_finishes columns were dropped as they were heavily skewed to the right.

Exploratory Data Analysis (EDA) included plotting boxplots of top 10 Masters finishers against the rest of the field, and Masters winners against the rest of the field. This provided a quick overview of important qualities that successful competitors had.

SMOTE and RandomUnderSampling were used to address the class imbalance problem, due to the significantly higher percentage of losers compared to winners. SMOTE was used to identify new winners based on nearest neighbors, while RandomUnderSampler reduced the size of the majority class through random removal. A combination of these two techniques helped in balancing the classes.

A StandardScaler was additionally applied, and three classifier models were tested on the data: RandomForestClassifier, SVC with a linear kernel, and SVC with an RBF kernel.

Recall was the main metric of interest to measure the model’s performance, as I wanted a high chance of the model correctly predicting true positives given the imbalanced data. The SVC linear model with tuned hyperparameters, discovered using GridSearch, achieved a recall of 0.61.

I then ran this trained model on the 2024 data, and the winner appeared in the top 5 results of the data, showing up over 80% of the time in the winning group, clearly indicating that there is merit to this model.

The model was saved using joblib.

app.py, index.html, results.html
The file app.py creates a Flask application that handles HTTP requests, processes data, interacts with the model, and renders HTML pages.

When the user visits the homepage, app.py serves index.html. The user then fills out the form outlined in the HTML file. The form data is sent to the /predict route in app.py via a POST request.

This data is processed and passed to the machine learning model to make the prediction.

After a prediction is made, app.py renders results.html and passes the prediction to it, thereby displaying the results.

This website allows users to input various statistics into a form and returns the likelihood that a given player will win the Masters Tournament.
