# FeedbackBot - Sentiment Analysis Telegram Bot

## Introduction

FeedbackBot is a Telegram bot that allows users to provide feedback, and it uses Natural Language Processing (NLP) to predict the sentiment of the feedbacks. The bot is built with Python (using FastAPI) for NLP tasks and JavaScript (using Telegraf.js) for Telegram bot functionalities. It utilizes a pre-trained NLP model to perform sentiment analysis on the feedbacks.

## Features

- Users can submit their feedback to the bot.
- The bot performs text preprocessing on the received feedback.
- Sentiment analysis is conducted using a pre-trained NLP model to predict the sentiment (positive/negative/neutral) of the feedback.
- The bot stores user feedback data in a MongoDB database using Mongoose.

## Prerequisites

Before running the FeedbackBot, you need to have the following installed:

- Python (for running app.py and main.py)
- Node.js (for running the Telegram bot JavaScript files)
- MongoDB (for storing user feedback data)

## Training the NLP Model

Before using the bot, you need to train the NLP model and create the sentiment_model_pipeline.pkl file.

1. Place your training data in the 'final.csv' file. Ensure the 'final.csv' file has a 'text' column containing the feedback text and a 'sentiment' column containing the corresponding sentiment labels (positive/negative/neutral).

2. Run the main.py file to train the model and generate the sentiment_model_pipeline.pkl file.

python main.py

## Usage

### Step 1: Start the Python NLP API

Run the app.py file to start the FastAPI server for the NLP model.

python app.py

The API will be available at http://127.0.0.1:8000.

### Step 2: Start the Telegram Bot

Run the bot.js file to start the Telegram bot using Telegraf.js.

cd bot
node bot.js

The bot will be active on Telegram and will respond to commands and collect user feedback.

### Step 3: Interacting with the Telegram Bot

- Start the bot by searching for it on Telegram and sending a message.
- The bot will request feedback from the user.
- After receiving feedback, it will process the text and predict the sentiment (positive/negative/neutral).
- The bot will store the user's feedback and sentiment analysis in the MongoDB database.

## Contributing

We welcome contributions to FeedbackBot! If you want to contribute, please create a pull request, and we will review it.

