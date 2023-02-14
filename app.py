# text preprocessing modules
from string import punctuation 
# text preprocessing modules
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from os.path import dirname, join, realpath
import joblib
import uvicorn
from fastapi import FastAPI
import sys
import json

app = FastAPI(
    title="Sentiment Model API",
    description="A simple API that use NLP model to predict the sentiment of the movie's reviews",
    version="0.1",
)

with open(
    join(dirname(realpath(__file__)), "sentiment_model_pipeline.pkl"), "rb"
) as f:
    model = joblib.load(f) ## Load the model

## We need to clean the text again becuase the user will enter the sentence in the form of a string instead of numbers.
## The sentence needs to be cleaned before it is passed to the model.

def text_cleaning(text):
    text = re.sub(r'@[A-Za-z0-9]+','',text)
    text = re.sub(r'#','',text)
    text = re.sub(r'RT[\s]+','',text)
    text = re.sub(r'https?:\/\/\S+','',text)
    text = re.sub(r'[^a-zA-Z ]',' ', text)
    text = text.lower()
    text = ''.join([c for c in text if c not in punctuation])
    
    stop_words = stopwords.words("english")
    text = text.split()
    text = [w for w in text if not w in stop_words]
    text = " ".join(text)
    
    text = text.split()
    lemmatizer = WordNetLemmatizer() 
    lemmatized_words = [lemmatizer.lemmatize(word) for word in text]
    text = " ".join(lemmatized_words)
    return(text)

# @app.get("/predict-review")
def predict_sentiment(review: str):
    """
    A simple function that receive a review content and predict the sentiment of the content.
    :param review:
    :return: prediction, probabilities
    """
    # clean the review
    cleaned_review = text_cleaning(review)
    # perform prediction
    prediction = model.predict([cleaned_review])
    ## We pass the sentence through the pipeline, i.e first tf-idf is done then model predictions are made.
    prediction = prediction.tolist()
    return prediction[0]
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        a = sys.argv[1]
        result = predict_sentiment(a)
        print(result,flush=True)