import streamlit as st
from src.utils import load_config, update_config
from src.passage_selector import run_pipeline
import tkinter as tk
from tkinter import filedialog
import os

def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder_selected = filedialog.askdirectory(master=root)
    return folder_selected

def main():
    st.markdown(
        """
        <style>
        .main .block-container {
            max-width: 1200px;
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Passage Selection Pipeline")

    config = load_config()

    query = st.text_input("Enter your query:", config['query'])

    if st.button('Select Folder'):
        folder_selected = select_folder()
        #st.text(f"Selected folder: {folder_selected}")
        config["document_folder_path"] = folder_selected

    if "document_folder_path" in config and config["document_folder_path"]:
        st.text(f"Selected folder path: {config['document_folder_path']}")

    retrieval_algorithm = st.selectbox("Document Retrieval Algorithm", ["bm25", "tfidf"], index=["bm25", "tfidf"].index(config['retrieval_algorithm']))
    ranking_method = st.selectbox("Passage Selection Method", ["sentence_transformers", "cohere_rerank"], index=["sentence_transformers", "cohere_rerank"].index(config['ranking_method']))

    updates = {
        "query": query,
        "retrieval_algorithm": retrieval_algorithm,
        "ranking_method": ranking_method,
        "document_folder_path": config.get("document_folder_path", "")
    }

    update_config(config, updates)

    if st.button("Run Pipeline"):
        query, relevant_passages = run_pipeline(config, debug=True)
        for result in relevant_passages:
            st.write(f"**Document:** {result[0]}")
            st.write(f"**Passage:** {result[1]}")
            st.write(f"**Score:** {result[2]}")
            st.write("---")

if __name__ == "__main__":
    main()
