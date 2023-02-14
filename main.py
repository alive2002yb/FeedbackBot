# import important modules
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from string import punctuation 

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 

import re
import pickle
import warnings
warnings.filterwarnings("ignore")

# Download dependency - One time run
'''for dependency in (
    "brown",
    "names",
    "wordnet",
    "averaged_perceptron_tagger",
    "universal_tagset",
    "stopwords",
    "punkt",
    "omw-1.4"
):
    nltk.download(dependency)'''

# seeding
np.random.seed(123)

df = pd.read_csv("final.csv")
print(df.shape)

# Dropping all columns except Class and Tweet. 

# Class: 

# 2 -> Neither
# 1 -> Offensive Language
# 0 -> hate_speech

#df = df.drop(['Unnamed: 0', 'count', 'hate_speech', 'offensive_language', 'neither'], axis=1)

stop_words =  stopwords.words('english')
def text_cleaning(text):
    # Clean the text, with the option to remove stop_words and to lemmatize word
    # Clean the text
    text = re.sub(r'@[A-Za-z0-9]+','',text) # Removing @mentions
    text = re.sub(r'#','',text) # Removing the '#' symbol
    text = re.sub(r'RT[\s]+','',text) # Removing RT
    text = re.sub(r'https?:\/\/\S+','',text) # Removing hyperlinks
    text = re.sub(r'[^a-zA-Z ]',' ', text) # Removing all the punctuations and numbers
    text = text.lower()
        
    # Remove punctuation from text
    text = ''.join([c for c in text if c not in punctuation])
    
    # Optionally, remove stop words
    # Stop words are the common words that are used in the dictionary like a, an and the etc
    stop_words = stopwords.words("english")
    text = text.split()
    text = [w for w in text if not w in stop_words]
    text = " ".join(text)
    
    # Optionally, shorten words to their stems
    text = text.split()
    lemmatizer = WordNetLemmatizer() 
    lemmatized_words = [lemmatizer.lemmatize(word) for word in text]
    text = " ".join(lemmatized_words)
    
    # Return a list of words
    return(text)

df["cleaned_tweet"] = df["text"].apply(text_cleaning)
## Applying the function on the text column

X = df["cleaned_tweet"] 
## The model will be trained on the cleaned tweets
y = df['label'].values
## There are three values that can be predicted:
## 0 -> hate_speech, 1 -> Abusive 2 -> Neither
print(df.head())
print(y)

# split data into train and validate
## The purpose of splitting the dataset into train and test set is that
## we can test our model on the test set after training it on the training set.
## We need real world data to verify our model, that is done by testig on the test set.

X_train, X_valid, y_train, y_valid = train_test_split(
    X,
    y,
    test_size=0.15, ## 15% of the data will be test data
    random_state=42,
    shuffle=True,
    stratify=y,## Ratio of the label will be same in both train and test set
)

## tf-idf stands for term-frequency inverse-document-frequency
## Term Frequency: How often a word appears in a document.
## Inverse Document Frequency: How often a word appears in all documents.

## We are converting the text into a vector of numbers with the help of tf-idf. Once that is done, we pass into the model.
sentiment_classifier = Pipeline(steps=[
                               ('pre_processing',TfidfVectorizer(lowercase=False)),
                                 ('logistic_regression', LogisticRegression(penalty = 'elasticnet', warm_start = True, max_iter = 1000,  C=1.3, solver='saga', l1_ratio=0.9))
                                 ])

## We need to fit the model on the train dataset
sentiment_classifier.fit(X_train,y_train)

## Once the model is trained, we can predict for the test dataset.
y_preds = sentiment_classifier.predict(X_valid)

## Get the accuracy score
print(accuracy_score(y_valid, y_preds))

saved_model=open('sentiment_model_pipeline.pkl','wb')

## We have exported the model as pickle file.
pickle.dump(sentiment_classifier, saved_model)
