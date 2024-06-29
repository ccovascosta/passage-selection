
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve_documents(query, documents, top_k=5, debug=False):
    doc_texts = [doc[1] for doc in documents]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(doc_texts)
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    ranked_indices = scores.argsort()[-top_k:][::-1]
    ranked_docs = [documents[i] for i in ranked_indices]

    if debug:
        for i, idx in enumerate(ranked_indices):
            print(f"Rank {i+1}: Document {documents[idx][0]} with score {scores[idx]}")

    return ranked_docs
