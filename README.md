# Passage Selection

This project implements a passage selection component. The goal is to develop an end-to-end pipeline that, given an utterance and a folder of documents, returns the top K documents with the most relevant passages extracted from each.

## Project Structure

passage-selection/
├── .git/
├── .gitignore
├── README.md
├── config.json
├── requirements.txt
├── myenv/
├── sample_data/
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── preprocess.py
│   ├── query_processing.py
│   ├── document_retrieval.py
│   ├── passage_extraction.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py
└── notebooks/
    └── passage_selection_test.ipynb



## Overview 

### Data Pipeline

 - *Data Ingestion:* The data_ingestion.py module handles extracting text from various document formats (PDF, DOCX, PPTX). This ensures we can process a wide variety of documents.
 - *Preprocessing:* The preprocess.py module cleans and preprocesses the text, removing stop words and non-alphanumeric characters, and converting text to lowercase. This standardizes the text for better retrieval performance.
 - *Query Processing:* The query_processing.py module processes the query in the same way as the document text, ensuring consistency.
- *Document Retrieval:* The document_retrieval.py module uses TF-IDF vectorization and cosine similarity to retrieve the top K relevant documents for the query.
 - *Passage Extraction:* The passage_extraction.py module uses a pre-trained question-answering model from Hugging Face's transformers library to extract the most relevant passages from the top documents.
 - *Main Pipeline:* The main.py module ties everything together, providing a single entry point to run the passage selection pipeline.

### Configuration File

The config.json file allows you to configure the pipeline parameters. Below is an example configuration file with explanations for each parameter:

```json
{
    "document_folder_path": "sample_data",
    "query_text": "What are the applications of generative AI?",
    "top_k": 5,
    "passage_max_length": 512,
    "passage_overlap": 50,
    "split_method": "tokens"
}
```
 - *document_folder_path:* The path to the folder containing the documents to be processed.
 - *query_text:* The query or utterance to search for in the documents.
 - *top_k:* The number of top documents to retrieve based on the query.
 - *passage_max_length:* The maximum length of each passage (in tokens or characters).
 - *passage_overlap:* The number of tokens or sentences to overlap between consecutive passages.
 - *split_method:* The method to split the text into passages (tokens or sentences).

### Installation

1. Clone the Repository:

```bash
git clone https://github.com/your-username/passage-selection.git
cd passage-selection
```

2. Create and Activate a Virtual Environment:

```bash
python -m venv myenv
myenv\Scripts\activate
```

3. Install Required Libraries:

```bash
pip install -r requirements.txt
```


### Usage

#### Option 1: Command Line

1. Ensure config.json is Set Up:

 - Edit the config.json file to point to the sample_data folder and provide an utterance.

2. Run the Pipeline from the Command Line:

```bash
python src/main.py
```

#### Option 2: Jupyter Notebook

1. Start Jupyter Notebook:

 - Navigate to the notebooks directory and start Jupyter Notebook:

```bash
cd notebooks
jupyter notebook
```

2. Open passage_selection_test.ipynb to interactively run and test the pipeline.

## Future Improvements

 - Enhanced Preprocessing: Implement more advanced text preprocessing techniques such as lemmatization and named entity recognition.
 - Advanced Retrieval Models: Explore the use of more advanced retrieval models.
 - Scalability: Optimize the pipeline for large-scale document processing and real-time performance.