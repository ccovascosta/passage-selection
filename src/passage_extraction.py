
from transformers import pipeline

retriever = pipeline("question-answering")

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

def extract_relevant_passages(query, documents, max_length=512, overlap=50, method='tokens'):
    results = []
    for doc_name, doc_text in documents:
        passages = split_text_into_passages(doc_text, max_length, overlap, method)
        for passage in passages:
            result = retriever(question=query, context=passage)
            results.append((doc_name, result['answer'], result['score']))
    results.sort(key=lambda x: x[2], reverse=True)
    return results
