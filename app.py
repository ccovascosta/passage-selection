import streamlit as st
from src.utils import load_config, update_config
from src.passage_selector import run_pipeline
import os

def main():
    st.title("Passage Selection Pipeline")

    config = load_config()

    document_folder_path = config["document_folder_path"]
    uploaded_file = st.file_uploader("Upload a dummy file from the target folder", type=['txt', 'pdf', 'docx', 'pptx'])
    
    if uploaded_file is not None:
        folder_selected = os.path.dirname(uploaded_file.name)
        st.text(f"Selected folder: {folder_selected}")
        document_folder_path = folder_selected

    query = st.text_input("Enter your query:", config["query"])
    preprocess_query = st.checkbox("Preprocess Query", config["preprocess_query"])
    top_k_docs = st.slider("Top K Documents", 1, 10, config["top_k_docs"])
    top_n_passages = st.slider("Top N Passages per Document", 1, 5, config["top_n_passages"])
    passage_max_length = st.slider("Passage Max Length", 100, 1000, config["passage_max_length"])
    passage_overlap = st.slider("Passage Overlap", 0, 100, config["passage_overlap"])
    split_method = st.selectbox("Split Method", ["tokens", "sentences"], index=["tokens", "sentences"].index(config["split_method"]))
    retrieval_algorithm = st.selectbox("Retrieval Algorithm", ["bm25", "tfidf"], index=["bm25", "tfidf"].index(config["retrieval_algorithm"]))
    ranking_method = st.selectbox("Ranking Method", ["sentence_transformers", "cohere_rerank"], index=["sentence_transformers", "cohere_rerank"].index(config["ranking_method"]))
    max_output_passages = st.slider("Final Number of Passages", 1, 20, config["max_output_passages"])

    updates = {
        "document_folder_path": document_folder_path,
        "query_text": query,
        "top_k_docs": top_k_docs,
        "top_n_passages": top_n_passages,
        "max_output_passages": max_output_passages,
        "passage_max_length": passage_max_length,
        "passage_overlap": passage_overlap,
        "split_method": split_method,
        "retrieval_algorithm": retrieval_algorithm,
        "ranking_method": ranking_method,
        "preprocess_query": preprocess_query
    }

    # Update the configuration with the new values
    update_config(config, updates)

    if st.button("Run Pipeline"):
        relevant_passages = run_pipeline(config, debug=True)
        for result in relevant_passages:
            st.write(f"Document: {result[0]}\nPassage: {result[1]}\nScore: {result[2]}\n")

if __name__ == "__main__":
    main()