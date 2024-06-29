
import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

def split_text_into_passages(text, max_length=512, overlap=50, method='tokens'):
    if method == 'tokens':
        words = text.split()
        passages = []
        current_passage = []
        for word in words:
            if len(current_passage) + len(word) <= max_length:
                current_passage.append(word)
            else:
                passages.append(" ".join(current_passage))
                current_passage = current_passage[-overlap:] + [word]
        if current_passage:
            passages.append(" ".join(current_passage))
    elif method == 'sentences':
        sentences = text.split('. ')
        passages = []
        current_passage = []
        for sentence in sentences:
            if len(" ".join(current_passage)) + len(sentence) <= max_length:
                current_passage.append(sentence)
            else:
                passages.append(". ".join(current_passage) + '.')
                current_passage = current_passage[-overlap:] + [sentence]
        if current_passage:
            passages.append(". ".join(current_passage) + '.')
    return passages

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text) #remove non-alphanumeric characters
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text