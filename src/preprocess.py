
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text) #remove non-alphanumeric characters
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text
