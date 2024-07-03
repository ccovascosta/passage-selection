import re
from nltk.corpus import stopwords
import nltk
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize

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

    elif method == 'semantic':
        passages = semantic_split(text, max_length)
    return passages

def semantic_split(text, max_length=512, model_name='all-MiniLM-L6-v2', similarity_threshold=0.75):
    model = SentenceTransformer(model_name)
    sentences = sent_tokenize(text)
    embeddings = model.encode(sentences, convert_to_tensor=True)
    similarities = [util.pytorch_cos_sim(embeddings[i], embeddings[i+1]).item() for i in range(len(embeddings)-1)]
    
    passages = []
    current_passage = sentences[0]
    
    for i, similarity in enumerate(similarities):
        if similarity < similarity_threshold or len(current_passage.split()) > max_length:
            passages.append(current_passage)
            current_passage = sentences[i+1]
        else:
            current_passage += ' ' + sentences[i+1]
    
    passages.append(current_passage)
    
    return passages

def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text)  # Remove non-alphanumeric characters
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text
