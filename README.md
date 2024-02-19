# BERT for Sentiment Analysis

## Features:
* Fine-tuned BERT model weights exported in a lightweight Flask API within Docker container ready for inference.
* Front-end app to accept text input from user. This input is sent to the model for classification.
* Backend MYSQL DB (separate Docker container) to store correctly classified texts with option to further fine-tune the BERT model with new data.
* Complete logging infrastructure to track inputs and performance of APP
* Incorrect predictions are not stored in DB as it would negatively imapct model performance

Using airline review data, I compared the performance of a Naive Bayes Classifier with a fine-tuned BERT model. 
The task is ultimately a binary classification with reviews being either negative or not-negative. The aim is to accurately classify any input text into either
'negative' or 'not-negative' categories.

Checkout the [notebooks](https://github.com/CMaxK/sentiment_app/tree/master/notebooks) for the model training and comparison process. It includes lots of comments to follow my thought process.

---

## To run:
1. Git clone this repo
2. re-run bert-training.ipynb to obtain model weights and save in a model_weights directory.
3. Create a **.env** file with MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_TABLE variables to store your specific DB credentials
4. run `docker-compose build && docker-compose up`
5. the app is hosted on port 5001 (enter **http://localhost:5001** into your browser)
   
---

## Homepage of App:
![image](https://github.com/CMaxK/sentiment_app/assets/71667581/00298c25-3d55-452c-8a16-05f607c920ad)

## Correct Positive App prediction:
![image](https://github.com/CMaxK/sentiment_app/assets/71667581/648c68f8-9e94-4c0b-b0e7-f5cb4dd30ca9)

## Returning Home once Feedback submitted:
![image](https://github.com/CMaxK/sentiment_app/assets/71667581/542120fa-6ed6-4549-aca7-ad89c0938ee1)

## Negative Prediction:
![image](https://github.com/CMaxK/sentiment_app/assets/71667581/b5c1b390-088b-4978-874f-34a8060932f0)
![image](https://github.com/CMaxK/sentiment_app/assets/71667581/0388a568-712f-4267-90de-fc9ec96097c1)

## Log outputs from within Docker container (`docker exec -it {CONTAINER_ID} /bin/sh && cat app.log`):
![image](https://github.com/CMaxK/sentiment_app/assets/71667581/647c7a9a-3934-4950-80f0-3c146ee20411)

## DB available for retraining BERT classifier:
![image](https://github.com/CMaxK/sentiment_app/assets/71667581/93fa52f3-e63a-402d-ac2d-ee2e81a4fffe)







