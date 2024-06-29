from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')



def vectorize_texts(texts):
    return embedding_model.encode(texts, convert_to_tensor=True)

def compute_similarity(query_vec, passage_vecs):
    return util.pytorch_cos_sim(query_vec, passage_vecs)

def extract_relevant_passages(query, doc_name, original_passages, preprocessed_passages, top_n=5):

    query_vec = embedding_model.encode(query, convert_to_tensor=True)
    passage_vecs = embedding_model.encode(preprocessed_passages, convert_to_tensor=True)
    
    cosine_scores = compute_similarity(query_vec, passage_vecs)[0]
    
    top_n_indices = cosine_scores.argsort(descending=True)[:top_n]
    top_passages = [(doc_name, original_passages[i], cosine_scores[i].item()) for i in top_n_indices]
    
    return top_passages