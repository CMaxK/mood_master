from flask import Flask, request, render_template, url_for, redirect
from sentiment_analysis import SentimentAnalysis
from datetime import datetime
from helpers.db import get_db_connection
import mysql.connector
from log import setup_logger
from dotenv import load_dotenv
import os

load_dotenv()
log = setup_logger()
database_name = os.getenv("MYSQL_DATABASE")
table_name = os.getenv("MYSQL_TABLE")
app = Flask(__name__)

# Create an instance of the SentimentAnalysis class with the model weights path
sentiment_analyzer = SentimentAnalysis('model_weights/bert_model_weights.pth')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def model_predict():
    text = request.form['text']
    predicted_class = sentiment_analyzer.perform_sentiment_analysis(text)
    sentiment_class = "green" if predicted_class == "Not Negative" else "red"

    return render_template('result.html', sentiment=predicted_class, sentiment_class=sentiment_class, original_text=text)

@app.route('/feedback', methods=['POST'])
def store_feedback():
    text = request.form.get('original_text')
    prediction_correct = request.form.get('prediction_correct')
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")

    log.info("***NEW RECORD RECEIVED***")
    log.info(f"Received text: {text}")
    log.info(f"Prediction correctness: {prediction_correct}")

    if text:
        # If 'prediction_correct' is 'yes' and the prediction was not negative, set target to 1
        # If 'prediction_correct' is 'yes' and the prediction was negative, set target to 0
        # If 'prediction_correct' is not 'yes', do nothing
        predicted_class = sentiment_analyzer.perform_sentiment_analysis(text)
        if prediction_correct == 'yes':
            if predicted_class == 'Not Negative':
                target = 1
            else:
                target = 0
        else:
            return redirect(url_for('index'))

        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute(f"USE {database_name}")
            # Insert the user feedback into the database
            insert_query = f"INSERT INTO {table_name} (text, target, created_at) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (text, target, formatted_datetime))
            db.commit()
            log.info("Feedback stored successfully.")

        except mysql.connector.Error as err:
            log.info(f"Database error: {err}")
            db.rollback()  # Rollback the transaction on error

        finally:
            cursor.close()
            db.close()

    else:
        log.info("no text")

    return redirect(url_for('thanks'))

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
    log.info('Starting the application')
