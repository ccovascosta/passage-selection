import cohere
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize
import re

cohere_client = cohere.Client('KstgNdd7d5wUyUYwoonCmUo1igq6KwLLLzL1EG4Q')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')


def is_valid_passage(passage):

    citation_words = re.findall(r'\b(et al\.|pp\.|vol\.|doi|ISSN|ISBN|In press)\b', passage)
    if len(citation_words) >= 3:  
        return False
    
    non_alphanumeric_ratio = len(re.findall(r'\W', passage)) / len(passage)
    if non_alphanumeric_ratio > 0.2:
        return False
    
    author_patterns = len(re.findall(r'\b[A-Z][a-z]+, [A-Z]\.\b', passage))
    if author_patterns >= 3:  # e.g. Last name, Initial.
        return False
    
    number_of_years = len(re.findall(r'\d{4}', passage))
    if number_of_years >= 3:
        return False

    return True

def vectorize_texts(texts):
    return embedding_model.encode(texts, convert_to_tensor=True)

def compute_similarity(query_vec, passage_vecs):
    return util.pytorch_cos_sim(query_vec, passage_vecs)

def cohere_rerank(query, passages, top_n):
    response = cohere_client.rerank(
        query=query,
        documents=[{"text": passage} for passage in passages],
        top_n=top_n,
        model='rerank-english-v3.0',
        return_documents=True

    )
    return response.results

def extract_relevant_passages(query, doc_name, original_passages, preprocessed_passages, top_n=5, method='sentence_transformers'):

    filtered_original_passages = [p for p in original_passages if is_valid_passage(p)]
    filtered_preprocessed_passages = [p for p in preprocessed_passages if is_valid_passage(p)]
   
    if method == 'sentence_transformers':
        query_vec = embedding_model.encode(query, convert_to_tensor=True)
        passage_vecs =  embedding_model.encode(filtered_original_passages, convert_to_tensor=True)
        cosine_scores = compute_similarity(query_vec, passage_vecs)[0]
        top_n_indices = cosine_scores.argsort(descending=True)[:top_n]
        top_passages = [(doc_name, filtered_original_passages[i], cosine_scores[i].item()) for i in top_n_indices]

    elif method == 'cohere_rerank':
        response = cohere_rerank(query, filtered_original_passages, top_n=top_n)
        ranked_passages = sorted(response, key=lambda x: x.relevance_score, reverse=True)[:top_n]
        top_passages = [(doc_name, passage.document.text if passage.document is not None else "", passage.relevance_score) for passage in ranked_passages]
        
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    return top_passages