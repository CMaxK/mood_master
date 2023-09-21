from flask import Flask, request, render_template, jsonify
from sentiment_analysis import SentimentAnalysis

app = Flask(__name__)

# Create an instance of the SentimentAnalysis class with the model weights path
sentiment_analyzer = SentimentAnalysis('model_weights/bert_model_weights.pth')

@app.route('/')
def index():
    # Your HTML template rendering logic here
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']

    # Perform sentiment analysis using the pre-trained model
    predicted_class = sentiment_analyzer.perform_sentiment_analysis(text)

    # Set sentiment_class based on the predicted sentiment
    sentiment_class = "green" if predicted_class == "Not Negative" else "red"

    # Pass the predicted class and sentiment_class as variables to the HTML template
    return render_template('result.html', sentiment=predicted_class, sentiment_class=sentiment_class)


if __name__ == '__main__':
    app.run(debug=True)
