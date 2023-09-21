from flask import Flask, request, render_template, url_for, redirect
from sentiment_analysis import SentimentAnalysis

import mysql.connector

import os
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path)

app = Flask(__name__)

db = mysql.connector.connect(
    host= os.environ.get('MYSQL_HOST'),
    user= os.environ.get('MYSQL_USER'),
    password= os.environ.get('MYSQL_PASSWORD'),
    database= os.environ.get('MYSQL_DB')
)
cursor = db.cursor()

# Create an instance of the SentimentAnalysis class with the model weights path
sentiment_analyzer = SentimentAnalysis('model_weights/bert_model_weights.pth')

@app.route('/')
def index():
    # Your HTML template rendering logic here
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def model_predict():
    text = request.form['text']
    predicted_class = sentiment_analyzer.perform_sentiment_analysis(text)

    # Set sentiment_class based on the predicted sentiment
    sentiment_class = "green" if predicted_class == "Not Negative" else "red"

    # Pass the predicted class and sentiment_class as variables to the HTML template
    return render_template('result.html', sentiment=predicted_class, sentiment_class=sentiment_class, original_text=text)

@app.route('/feedback', methods=['POST'])
def store_feedback():
    # Retrieve user input, prediction correctness, and original text
    text = request.form.get('original_text')
    prediction_correct = request.form.get('prediction_correct')

    print(f"Received text: {text}")
    print(f"Prediction correctness: {prediction_correct}")

    # Ensure that 'text' is not empty or None
    if text:
        # Determine the target value based on 'prediction_correct'
        # If 'prediction_correct' is 'yes', set target to 1 (not negative)
        # If 'prediction_correct' is not 'yes', set target to 0 (negative)
        target = 1 if prediction_correct == 'yes' else 0

        try:
            # Insert the user feedback into the database
            insert_query = "INSERT INTO input_data (text, target) VALUES (%s, %s)"
            cursor.execute(insert_query, (text, target))

            # Commit the transaction
            db.commit()

            # Debug message to indicate success
            print("Feedback stored successfully.")

        except mysql.connector.Error as err:
            # Handle any database-related errors
            print(f"Database error: {err}")
            db.rollback()  # Rollback the transaction on error

    else:
        print("no text")

    return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(debug=True)
