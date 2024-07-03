
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi

def retrieve_documents(query, documents, top_k=5, algorithm="tfidf", debug=False):
    doc_texts = [doc[1] for doc in documents]

    if algorithm == "tfidf":
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(doc_texts)
        query_vec = vectorizer.transform([query])
        scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    elif algorithm == "bm25":
        tokenized_docs = [doc.split() for doc in doc_texts]
        bm25 = BM25Okapi(tokenized_docs)
        tokenized_query = query.split()
        scores = bm25.get_scores(tokenized_query)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    ranked_indices = scores.argsort()[-top_k:][::-1]
    ranked_docs = [documents[i] for i in ranked_indices]

    if debug:
        for i, idx in enumerate(ranked_indices):
            print(f"Rank {i+1}: Document {documents[idx][0]} with score {scores[idx]}")

    return ranked_docs
