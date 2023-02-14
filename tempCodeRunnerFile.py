def predict_sentiment(review: str):
    """
    A simple function that receive a review content and predict the sentiment of the content.
    :param review:
    :return: prediction, probabilities
    """
    # clean the review
    cleaned_review = text_cleaning(review)
    review="Fuck"
    print(cleaned_review)
    # perform prediction
    prediction = model.predict([cleaned_review])
    ## We pass the sentence through the pipeline, i.e first tf-idf is done then model predictions are made.
    prediction = prediction.tolist()
    print(prediction[0])
    judgements = {2: "Normal", 1: "Offensive Language", 0: "Hate Speech"}
    print(judgements)
    return {"Prediction": judgements[int(prediction[0])]}