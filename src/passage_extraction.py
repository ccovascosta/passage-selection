import cohere
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from nltk.tokenize import sent_tokenize
import re

cohere_client = cohere.Client('KstgNdd7d5wUyUYwoonCmUo1igq6KwLLLzL1EG4Q')
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
qa_pipeline = pipeline('question-answering', model='distilbert-base-cased-distilled-squad')


def is_valid_passage(passage):

    if len(passage) == 0:
        return False

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

def is_redundant(new_passage, selected_passages, threshold=0.8):
    if not selected_passages:
        return False
    new_vec = embedding_model.encode([new_passage], convert_to_tensor=True)
    selected_vecs = embedding_model.encode(selected_passages, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(new_vec, selected_vecs)[0]
    return any(similarity > threshold for similarity in similarities)

def extract_relevant_passages(query, doc_name, original_passages, preprocessed_passages, top_n=5, method='sentence_transformers'):

    filtered_original_passages = [p for p in original_passages if is_valid_passage(p)]
    filtered_preprocessed_passages = [p for p in preprocessed_passages if is_valid_passage(p)]
   
    if method == 'sentence_transformers':
        query_vec = embedding_model.encode(query, convert_to_tensor=True)
        passage_vecs =  embedding_model.encode(filtered_original_passages, convert_to_tensor=True)
        cosine_scores = compute_similarity(query_vec, passage_vecs)[0]
        ranked_indices = cosine_scores.argsort(descending=True)
        ranked_passages = [(doc_name, filtered_original_passages[i], cosine_scores[i].item()) for i in ranked_indices]

    elif method == 'cohere_rerank':
        response = cohere_rerank(query, filtered_original_passages, top_n=len(filtered_original_passages))
        ranked_passages = sorted(response, key=lambda x: x.relevance_score, reverse=True)
        ranked_passages = [(doc_name, passage.document.text if passage.document is not None else "", passage.relevance_score) for passage in ranked_passages]
        
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    selected_passages = []
    for passage in ranked_passages:
        if not is_redundant(passage[1], [p[1] for p in selected_passages]):
            selected_passages.append(passage)
            if len(selected_passages) >= top_n:
                break
    
    return selected_passages