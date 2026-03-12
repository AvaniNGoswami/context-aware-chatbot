import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

import os
# print(os.getcwd())


# Load the saved model and vectorizer
os.chdir(r"C:/Users/Avani N. Goswami/Desktop/jupyter notebook/sentiment analysis of social media data/twitter")
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open(r"C:/Users/Avani N. Goswami/Desktop/jupyter notebook/sentiment analysis of social media data/twitter/vectorize.pkl", 'rb'))

def clean_text(text):
    ps = PorterStemmer()
    stop_words = stopwords.words('english')
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if word not in stop_words]
    return ' '.join(text)



# if st.button("Analyze"):
def analyze(input_text):
    cleaned = clean_text(input_text)
    vectorized = vectorizer.transform([cleaned]).toarray()
    result = model.predict(vectorized)
    sentiment = ''

    # label = "Positive" if result[0] == 1 else "Neutral/Negative"
    if result[0]==3:
        sentiment = 'Positive'
    elif result[0]==2:
        sentiment = 'Neutral'
    else:
        if result[0]==1:
            sentiment = 'Negative'


    return {'predicted_sentiment': sentiment}



