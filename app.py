from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import joblib

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('masters_winner_model.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():

    data = {
        'Avg_score':request.form.get('Avg_score'),
        'Drive Avg':request.form.get('Drive Avg'),
        '%_of_fairways_hit':request.form.get('%_of_fairways_hit'),
        'Putts per round':request.form.get('Putts per round'),
        'GIR %':request.form.get('GIR %'),
        'Scramble %':request.form.get('Scramble %'),
        'Bounce_Back %':request.form.get('Bounce_Back %'),
        'Total Strokes Gained':request.form.get('Total Strokes Gained'),
        'SG:OTT':request.form.get('SG:OTT'),
        'SG:ARG':request.form.get('SG:ARG'),
        'SG:TTG':request.form.get('SG:TTG'),
        'SG:APG':request.form.get('SG:APG'),
        'SG:PUTT':request.form.get('SG:PUTT'),
        'Par 3 Score':request.form.get('Par 3 Score'),
        'Par 4 score':request.form.get('Par 4 score'),
        'Par 5 score':request.form.get('Par 5 score')
    }

    data_df = pd.DataFrame([data])

    predictors = ['Avg_score', 'Drive Avg', '%_of_fairways_hit', 'Putts per round', 'GIR %', 'Scramble %',
                'Bounce_Back %', 'Total Strokes Gained', 'SG:OTT', 'SG:ARG', 'SG:TTG', 'SG:APG',
                'SG:PUTT', 'Par 3 Score', 'Par 4 score', 'Par 5 score']

    for col in predictors:
        if col not in data_df.columns:
            data_df[col] = np.nan

    for col in predictors:
        if data_df[col].dtype == 'object':
            data_df[col] = pd.to_numeric(data_df[col].str.replace('%', ''), errors = 'coerce')

    data_df = data_df[predictors]

    prediction_proba = model.predict_proba(data_df)[:, 1]
    probability = round(prediction_proba[0] * 100, 2)
    return render_template('results.html', probability = probability)

if __name__ == '__main__':
    app.run(debug=True)
