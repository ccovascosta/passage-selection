# Passage Selection

This project implements a passage selection component. The goal is to develop an end-to-end pipeline that, given an utterance and a folder of documents, returns the top K documents with the most relevant passages extracted from each.

## Project Structure

```plaintext
passage-selection/
├── .git/
├── .gitignore
├── README.md
├── config.json
├── requirements.txt
├── myenv/
├── sample_data/
└── evaluation_data/
├── processed_folder/
├── images/
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py
│   ├── document_retrieval.py
│   ├── utils.py
│   ├── passage_extraction.py
│   ├── passage_selector.py
│   ├── preprocess.py
│   ├── query_processing.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py
└── notebooks/
    └── passage_selection_test.ipynb
```

## Overview 

### Use Cases

 - Passage Selector Pipeline: This is intended for passage selection task. This pipelines allows a user to point to a folder of documents and a query, and retrieve the top K documents with the most relevant passages.
 - Evaluation Pipeline (to-do): This is designed to evaluate different document retrieval and passage selection approaches using the [MS MARCO dataset](https://microsoft.github.io/msmarco/Datasets.html).

### Data Pipeline

 - **Data ingestion:** The data_ingestion.py module handles extracting text from various document formats (PDF, DOCX, PPTX).
 - **Preprocessing:** The preprocess.py module cleans and preprocesses the text, removing stop words and non-alphanumeric characters, converting text to lowercase, and splitting the text into passages.
 - **Query processing:** The query_processing.py is an optional module that processes the query in the same way as the document text.
 - **Document Retrieval:** The document_retrieval.py module supports different algorithms:
     - TF-IDF: A traditional method that uses term frequency-inverse document frequency to rank documents. If this algorithm is selected, the retrieval module will use TF-IDF vectorization and cosine similarity to retrieve the top K relevant documents for the query.
     - [BM25](https://www.cs.otago.ac.nz/homepages/andrew/papers/2014-2.pdf): uses [rank-bm25](https://pypi.org/project/rank-bm25/) python library, which provides a collection of BM25 algorithms for querying a set of documents and returning the ones most relevant to the query.
 - **Passage extraction:** The passage_extraction.py module supports:
     - Sentence Transformers: Uses [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) sentence transformer model, which maps sentence and paragraphs to a 384 dimensional dense vector space for semantic search in order to extract the most relevant passages from the top documents.
     - Cohere Rerank: Uses the [Cohere Rerank](https://cohere.com/blog/rerank) for passage selection based on their relevance to the query.
 - **Passage Selector pipeline:** The main.py module ties everything together, providing a single entry point to run the passage selection pipeline.
 - **Evaluation pipeline (to-do):** The evaluation.py module uses the MS MARCO dataset to evaluate and compare different document retrieval and passage selection methods.

### Passage Processing Functions

 - **Passage Splitting:** The *split_text_into_passages* function splits a text into smaller passages using various methods, including token-based splitting, sentence-based splitting, and semantic splitting with a sentence transformer model. The goal is to create manageable chunks of text that can be independently evaluated for relevance.

 - **Passage Validity Check:** The *is_valid_passage* function checks the validity of a passage by applying several heuristics, such as checking for a high ratio of non-alphanumeric characters, the presence of certain citation patterns, and the frequency of years or author patterns. Passages failing these checks are considered invalid.

 - **Passage Extraction:** The *extract_relevant_passages* function extracts the most relevant passages from the top-ranked documents. It uses either sentence transformers or Cohere's reranking model to rank the passages and then filters out redundant passages to ensure diversity in the results.

 - **Redundancy Check:** The *is_redundant* function checks if a passage is redundant by comparing it to a list of already selected passages using cosine similarity of their embeddings. If the similarity score is above a certain threshold, the passage is considered redundant and not included in the final results.

### Configuration File

The config.json file is used to configure the pipeline parameters. Below is an example configuration file with explanations for each parameter:

```json
{
    "document_folder_path": "sample_data",
    "query_text": "What are the applications of generative AI?",
    "top_k_docs": 5,
    "top_n_passages": 2,
    "max_output_passages": 5,
    "passage_max_length": 512,
    "passage_overlap": 50,
    "split_method": "tokens",
    "retrieval_algorithm": "tfidf",
    "ranking_method": "sentence_transformers",
    "output_file": "results.json"
}
```

 - **document_folder_path:** The path to the folder containing the documents to be processed.
 - **query_text:** The query or utterance to search for in the documents.
 - **top_k:** The number of top documents to retrieve based on the query.
 - **top_n_passages:** The number of top passages to extract from each top document.
 - **final_n_passages:** The final number of passages to return.
 - **passage_max_length:** The maximum length of each passage (in tokens or sentences).
 - **passage_overlap:** The number of tokens or sentences to overlap between consecutive passages.
 - **split_method:** The method to split the text into passages (tokens or sentences).
 - **retrieval_algorithm:** The algorithm for document retrieval (tfidf or bm25).
 - **ranking_method:** The method for passage ranking (sentence_transformers or cohere_rerank).
 - **output_file:** The file to write the results to.

### Installation

1. Clone the Repository:

```bash
git clone https://github.com/ccovascosta/passage-selection.git
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

4. Cohere API Setup (Optional)

To use the Cohere rerank method, you need to get an API key from Cohere:

    4.1. Sign up for a free account at Cohere.
    4.2. After signing up, go to the [API keys section](https://dashboard.cohere.com/api-keys) in your Cohere dashboard.
    4.3. Copy the API key provided.
    4.4. Update the API key in the [src/passage_extraction.py](https://github.com/ccovascosta/passage-selection/blob/main/src/passage_extraction.py) file:

```python
cohere_client = cohere.Client('api_key')
```

### Usage

#### Passage selector Pipeline

#### Option 1: Command Line

1. Ensure config.json is set up:

    - Edit the config.json file to point to the sample_data folder and provide an utterance.

2. Run the pipeline from the command Lline:

```bash
python src/main.py
```

#### Option 2: Streamlit Interface

1. Run the Streamlit App:

```bash
streamlit run app.py
```

2. Interact with the Web Interface to Select Parameters and Run the Pipeline:

![Passage Selection Interface](images/passage_selection_interface.png)

#### Option 3: Jupyter Notebook

1. Start Jupyter notebook:

 - Navigate to the notebooks directory and start Jupyter notebook:

```bash
cd notebooks
jupyter notebook
```

2. Create a notebook to interactively run and test the pipeline.

#### Evaluation Pipeline

1. Ensure the Evaluation Data is in Place:
    - Download and extract the [MS MARCO dataset](https://microsoft.github.io/msmarco/Datasets.html) into the evaluation_data folder.
Run the Evaluation Script:

## Future Improvements

 - **Support other file types:** Implement text extraction function for other types of files such as emails, text files, transcriptions.
 - **Enhanced preprocessing:** Implement more advanced text preprocessing techniques.
 - **Document retrieval:** Explore other approaches for retrieving the top K documents, such Learn to Rank.
 - **Improved passage extraction:** Use more sophisticated models or techniques for passage extraction to improve the accuracy and relevance of the selected passages. Also test other approaches do split the text into passages to avoid unnecessary sentences and words.  
 - **Evaluation metrics:** Assess the system's performance using evaluation metrics for document retrieval and passage extraction, such as Mean Reciprocal Rank (MRR), Normalized Discounted Cumulative Gain (nDCG), and Precision@k. Leverage publicly available datasets, such as MS MARCO, for this evaluation.
 - **Scalability:** Optimize the pipeline for large-scale document processing and real-time performance using Azure.

 ## Example Output

Here is an example of how the passage selection pipeline processes documents and extracts relevant passages based on the query:

```json
 {
    "document_folder_path": "sample_data",
    "query_text": "How does the consumption of tea and coffee impact health?",
    "top_k_docs": 3,
    "top_n_passages": 2,
    "passage_max_length": 250,
    "passage_overlap": 25,
    "split_method": "tokens"
}
```

```plaintext
Reading document: A Comprehensive Overview of Large Language Models.pdf
Preprocessing document: A Comprehensive Overview of Large Language Models.pdf
Reading document: A Survey of Large Language Models.pdf
Preprocessing document: A Survey of Large Language Models.pdf
Reading document: beneficial and adverse effects of caffeine consumption.pdf
Preprocessing document: beneficial and adverse effects of caffeine consumption.pdf
Reading document: Beneficialeffectsofgreentea.Areview.pdf
Preprocessing document: Beneficialeffectsofgreentea.Areview.pdf
Reading document: BERT Pre-training of Deep Bidirectional Transformers for Language Understanding.pdf
Preprocessing document: BERT Pre-training of Deep Bidirectional Transformers for Language Understanding.pdf
Reading document: Exploring the Limits of Small Language Models.pdf
Preprocessing document: Exploring the Limits of Small Language Models.pdf
Reading document: Getting started with Large Language Models.docx
Preprocessing document: Getting started with Large Language Models.docx
Reading document: GitHub Copilot - Presentation by vinitshahdeo.pdf
Preprocessing document: GitHub Copilot - Presentation by vinitshahdeo.pdf
Reading document: Green Tea -  Potential Health Benefits.pdf
Preprocessing document: Green Tea -  Potential Health Benefits.pdf
Reading document: Healthy properties of green and white teas an update.pdf
Preprocessing document: Healthy properties of green and white teas an update.pdf
Reading document: History of Privacy.pdf
Preprocessing document: History of Privacy.pdf
Reading document: Language Models are Few-Shot Learners.pdf
Preprocessing document: Language Models are Few-Shot Learners.pdf
Reading document: Large Language Models for Dummies.pptx
Preprocessing document: Large Language Models for Dummies.pptx
Reading document: Large language models SIMPLIFIED.pptx
Preprocessing document: Large language models SIMPLIFIED.pptx
Reading document: LLM (Large Language Model) inference multi-cloud support.docx
Preprocessing document: LLM (Large Language Model) inference multi-cloud support.docx
Reading document: Microsoft-Cloud-for-Nonprofit-Overview.pdf
Preprocessing document: Microsoft-Cloud-for-Nonprofit-Overview.pdf
Reading document: MiniCPM - Unveiling the Potential of Small Language Models.pdf
Preprocessing document: MiniCPM - Unveiling the Potential of Small Language Models.pdf
Reading document: TinyStories - How Small Can Language Models Be and Still Speak.pdf
Preprocessing document: TinyStories - How Small Can Language Models Be and Still Speak.pdf
Reading document: What is Privacy That s the Wrong Question
Unsupported file format: sample_data\What is Privacy That s the Wrong Question
All documents have been processed.
Evaluating the top 3 most relevant documents
Rank 1: Document {'filename': 'beneficial and adverse effects of caffeine consumption.pdf', 'type': 'pdf', 'title': None, 'authors': 'marcia cristina lazzari', 'lastmodifiedtime': "D:20211024081204-03'00'"} with score 11.311782681128175
Rank 2: Document {'filename': 'Beneficialeffectsofgreentea.Areview.pdf', 'type': 'pdf', 'title': '', 'authors': '', 'lastmodifiedtime': 'D:20060323172315Z'} with score 10.581208732223748
Rank 3: Document {'filename': 'Healthy properties of green and white teas an update.pdf', 'type': 'pdf', 'title': None, 'authors': 'Marta', 'lastmodifiedtime': "D:20181204083145+01'00'"} with score 6.572854814980699
Extracting relevant passages from the top documents
Extracting passages from document: beneficial and adverse effects of caffeine consumption.pdf
Extracting passages from document: Beneficialeffectsofgreentea.Areview.pdf
Extracting passages from document: Healthy properties of green and white teas an update.pdf

Query: How does the consumption of tea and coffee impact cardiovascular and cognitive health?

Document: Beneficialeffectsofgreentea.Areview.pdf
Passage: in-vestigations on this beverage and its constituents have beenunderway for less than three decades [4]. In vitro and animal studies, and clinical trials employing putative intermediaryindicators of disease, particularly biomarkers of oxidative stressstatus, provide strong evidence that green tea polyphenols(GTP) may play a role in the risk and pathogenesis of severalchronic diseases, especially cardiovascular disease and cancer,and related pathologies. In addition, several studies suggest abeneficial impact of green tea intake on bone density, cognitivefunction, dental caries and kidney stones, among other effects[4–5]. Over the last years, numerous epidemiological and clin-ical studies have revealed several physiological responses togreen tea which may be relevant to the promotion of health andthe prevention or treatment of some chronic diseases. However,the results from epidemiological and clinical studies of therelationship between green tea consumption and human healthare mixed. For example, conflicting results between humanstudies may arise in part, from ignoring socioeconomic andlifestyle factors as well as by inadequate methodology to definetea preparation and intake [2,4–7]. Foodstuff can be regarded as functional if it is satisfactorily demonstrated to affect beneficially one or more target functionsin the body, beyond adequate nutritional effects in a way whichis relevant to either the state of well-being and health or thereduction of the risk of a disease [5,8–9], so green tea has beenproved to have functional properties and at present, its con-sumption is widely recommended. The aim of this article is to revise the most recent studies on green tea beneficial effects and to evaluate its
Score: 0.42697853

Document: Healthy properties of green and white teas an update.pdf
Passage: women since tea can reduce the bioavailability of folic acid. In general, their consumption should be reduced in people with anemia due to the possible interaction of tea tannins with Fe and especially in the case of megaloblastic anemia.28 The presence of aluminum may be rather elevated in some types of tea because of a notable influence of cultivated and processed soil levels.16 On the other hand, drinking too hot tea may increase the r isk of esophageal cancer.118 Finally, a very high consumption of green or white tea would lead to excessive intake of flavonoids, which would give rise to the formation of ROS that would cause damage in DNA, lipid membranes and proteins.117 4. CONCLUSIONS The health e ffects associated with the consumption of green and white teas include protection against hypertension and cardiovascular diseases, promotion of oral health, control of body weight, antibacterial and antiviral activity, protection against UV ra diation, increase of bone mineral density, and antifibrotic and neuroprotective properties, among others. These e ffects are related to their high content of polyphenols and in particular catechins, where EGCG stands out due to its high antioxidant potentia l, which even surpasses that found in vitamins C and E. The e ffects are also related to the presence of caffeine and L -theanine, an amino acid with interesting biological effects. Green and white teas may also be a source of some minerals, including Mn and F. Recent studies indicate that the
Score: 0.32788348

Document: Healthy properties of green and white teas an update.pdf
Passage: studies have revealed that green and white teas have positive biological activities against chronic diseases such as cancer, metabolic syndrome, type 2 diabetes, cardiovascular and neurodegenerative pathologies, among others. These protective properties are related to the potent antioxidant and anti- inflammatory activities of xanthic bases (ca ffeine and theophylline), essential oils (green tea and white tea are the two types of tea with the highest content), minerals (F, Mn, Cr), L -theanine and, mostly, catechins and other phenolic compounds.12,32 Caffeine acts on the central nervous system by stimulatin g attention, facilitating the association of ideas and reducing the sensation of fatigue. Some of the e ffects caused by ca ffeine are influenced by the content of theophylline, which also has inotrope, vasodilator, diuretic and bronchodilator action.12,25 Essential oils, which are abundant in green tea and white tea, facilitate digestion.12 Catechins and in particular EGCG have low bioavailability when orally ingested.33 Only a small percentage is absorbed at the level of the small intestine and passes into the bloodstream, reaching maximum plasma concentrations between 1 –3 hours after consumption. Some authors indicate that the secondary metabolites derived from the intake of flavonoids could be detected in blood and urine. For that reason, it is thought tha t the observed biological e ffects are possibly due to these secondary metabolites rather than the flavonoids themselves, which are detected in their original form in very low quantities.34 The bioavailability of phenolic tea compounds has been
Score: 0.10781264

Results have been written to results.json
``` 