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
```


## Overview 

### Data Pipeline

 - *Data ingestion:* The data_ingestion.py module handles extracting text from various document formats (PDF, DOCX, PPTX).
 - *Preprocessing:* The preprocess.py module cleans and preprocesses the text, removing stop words and non-alphanumeric characters, converting text to lowercase, and splitting the text into passages. This standardizes the text for better retrieval performance.
 - *Query processing:* The query_processing.py module processes the query in the same way as the document text, ensuring consistency.
- *Document retrieval:* The document_retrieval.py module uses TF-IDF vectorization and cosine similarity to retrieve the top K relevant documents for the query.
 - *Passage extraction:* The passage_extraction.py module uses Sentence Transformers for semantic similarity to extract the most relevant passages from the top documents.
 - *Main pipeline:* The main.py module ties everything together, providing a single entry point to run the passage selection pipeline.

### Configuration File

The config.json file is used to configure the pipeline parameters. Below is an example configuration file with explanations for each parameter:

```json
{
    "document_folder_path": "sample_data",
    "query_text": "How does regular consumption of tea impact cognitive function and cardiovascular health?",
    "top_k_docs": 5,
    "top_n_passages": 3,
    "passage_max_length": 300,
    "passage_overlap": 50,
    "split_method": "tokens"
}
```

 - *document_folder_path:* The path to the folder containing the documents to be processed.
 - *query_text:* The query or utterance to search for in the documents.
 - *top_k:* The number of top documents to retrieve based on the query.
 - *top_n_passages:* The number of top passages to extract from each top document.
 - *passage_max_length:* The maximum length of each passage (in tokens or sentences).
 - *passage_overlap:* The number of tokens or sentences to overlap between consecutive passages.
 - *split_method:* The method to split the text into passages (tokens or sentences).

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


### Usage

#### Option 1: Command Line

1. Ensure config.json is set up:

 - Edit the config.json file to point to the sample_data folder and provide an utterance.

2. Run the pipeline from the command Lline:

```bash
python src/main.py
```

#### Option 2: Jupyter Notebook

1. Start Jupyter notebook:

 - Navigate to the notebooks directory and start Jupyter notebook:

```bash
cd notebooks
jupyter notebook
```

2. Create a notebook to interactively run and test the pipeline.

## Future Improvements

 - Support other file types: Implement text extraction function for other types of files such as emails, text files, transcriptions.
 - Enhanced preprocessing: Implement more advanced text preprocessing techniques such as lemmatization.
 - Document retrieval: Explore other approaches for retrieving the top K documents, such as using other algorithms, such as BM25, or framing the problem as a binary classification to retrieve the documents with highest score (likelihood to contain relevant information).
 - Improved passage extraction: Use more sophisticated models or techniques for passage extraction to improve the accuracy and relevance of the selected passages. Also test other approaches do split the text into passages to avoid unnecessary sentences and words.  
 - Evaluation metrics: Assess the system's performance using evaluation metrics for document retrieval and for passage extraction.
 - Scalability: Optimize the pipeline for large-scale document processing and real-time performance.

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

Rank 1: Document {'filename': 'Beneficialeffectsofgreentea.Areview.pdf', 'type': 'pdf', 'title': '', 'authors': '', 'lastmodifiedtime': 'D:20060323172315Z'} with score 0.4368201468961804
Rank 2: Document {'filename': 'Healthy properties of green and white teas an update.pdf', 'type': 'pdf', 'title': None, 'authors': 'Marta', 'lastmodifiedtime': "D:20181204083145+01'00'"} with score 0.41357147527837784
Rank 3: Document {'filename': 'Green Tea -  Potential Health Benefits.pdf', 'type': 'pdf', 'title': None, 'authors': None, 'lastmodifiedtime': "D:20090324144108-05'00'"} with score 0.3619179436827994

Extracting relevant passages from the top documents
Extracting passages from document: Beneficialeffectsofgreentea.Areview.pdf
Document: Beneficialeffectsofgreentea.Areview.pdf
Passage: alsomore energetic, do contain more caffeine (green tea containsless caffeine than black tea, coffee or cola soft-drinks), are richin additives and/or CO 2. While no single food item can be expected to provide a significant effect on public health, it isimportant to note that a modest effect between a dietary com-ponent and a disease having a major impact on the mostprevalent causes of morbidity and mortality, i.e., cancer andheart disease, should merit substantial attention. Taking all thisinto account, it would be advisable to consider the regularconsumption of green tea in Western diets. ACKNOWLEDGMENT We thank M.J. Martinez-Vique for revising the English grammar of the original manuscript. We thank Antiguo Tosta-dero (specialized tea shop) for its cooperation and interest inthis research.REFERENCES 1. Costa LM, Gouveia ST, Nobrega JA: Comparison of heating extraction procedures for Al, Ca, Mg and Mn in tea samples. AnnSci 18:313–318, 2002. 2. Rietveld A, Wiseman S: Antioxidant effects of tea: Evidence from human clinical trials. J Nutr 133:3275–3284, 2003. 3. Willson KC: “Coffee, Cocoa and Tea.” New York: CABI Pub- lishing, 1999. 4. McKay DL, Blumberg JB: The role of tea in human health: An update. J Am Coll Nutr 21:1–13, 2002. 5. Wu CD, Wei GX: Tea as a functional food for oral health. Nutrition 18:443–444, 2002. 6. Zuo Y, Chen H, Deng Y: Simultaneous determination of cat- echins, caffeine and gallic acids in green, Oolong, black andPu-erh teas using HPLC with a photodiode array detector. Ta- lanta
Score: 0.6877859830856323

Document: Beneficialeffectsofgreentea.Areview.pdf
Passage: presence in black and green tea, some studies revealed the high capacity of this plant to accumulateAl. This aspect is important for patients with renal failuresbecause Al can be accumulated by the body, resulting inneurological diseases; it is therefore necessary to control theintake of food with high amounts of this metal [1]. The possibleconnection between elevated tissue Al content and problemssuch as osteomalacia and neurodegenerative disorders (i.e.,Alzheimer’s disease) has awakened interest in Al intake viadiet [158]. Minoia et al. [159] found concentrations of Al in green and black teas (as infusions) accounting for 431–2239 /H9262g/L, whereas in coffee they found lower concentrations (9.1– 30.8/H9262g/L). In a study carried out in Italy, these authors estimated the tea contribution to the total Al dietary intake as665 /H9262g/week (considering a weekly mean consumption of 2 cups). According to several authors, Al dietary intake must notexceed 6 mg/day in order to avoid potentially toxic levels[160]. Lo ´pez et al. [158] evaluated Al presence in food and beverages widely consumed in Spain, and found that Al levelsin tea ranged from 43.42 to 58.04 /H9262g/g referred to dry weight of the solid product, and from 13.91 to 27.45 /H9262g/L in the corresponding infusions; levels in coffee samples varied be-tween 25.6 and 29.08 /H9262g/g referred to dry weight of the solid product, and from 7.12 to 9.14 /H9262g/L in the corresponding infusions. Costa et al. [1] observed that black tea contains nearly six-fold more Al than green tea, and the
Score: 0.6832461357116699

Extracting passages from document: Healthy properties of green and white teas an update.pdf
Document: Healthy properties of green and white teas an update.pdf
Passage: women since tea can reduce the bioavailability of folic acid. In general, their consumption should be reduced in people with anemia due to the possible interaction of tea tannins with Fe and especially in the case of megaloblastic anemia.28 The presence of aluminum may be rather elevated in some types of tea because of a notable influence of cultivated and processed soil levels.16 On the other hand, drinking too hot tea may increase the r isk of esophageal cancer.118 Finally, a very high consumption of green or white tea would lead to excessive intake of flavonoids, which would give rise to the formation of ROS that would cause damage in DNA, lipid membranes and proteins.117 4. CONCLUSIONS The health e ffects associated with the consumption of green and white teas include protection against hypertension and cardiovascular diseases, promotion of oral health, control of body weight, antibacterial and antiviral activity, protection against UV ra diation, increase of bone mineral density, and antifibrotic and neuroprotective properties, among others. These e ffects are related to their high content of polyphenols and in particular catechins, where EGCG stands out due to its high antioxidant potentia l, which even surpasses that found in vitamins C and E. The e ffects are also related to the presence of caffeine and L -theanine, an amino acid with interesting biological effects. Green and white teas may also be a source of some minerals, including Mn and F. Recent studies indicate that the
Score: 0.6720261573791504

Document: Healthy properties of green and white teas an update.pdf
Passage: Moreover, it would be interesting to carry out additional studies with a habitual consumption extended in time more than studies designed with a very high consumption during a short period of time. For instance, cancer studies generally compare a low or no consumption versus a high consumption (even 10 cups per day). Regarding the research carried out with extracts, a better control of factors such as dose or formulation is necessary. This fact is essential in order to better identify the product tested and the population which it can exercise the benefit in. In conclusion, further research and well -designed additional studies (observational, epidemiological and nutritional Pastoriza et al. / Food & Function 8 (2017) 2650-2662 pag. 9 intervention) are needed to define the current magnitude of health e ffects of tea, to establish the range of safety of the consumption associated with beneficial effects and to elucidate the possible mechanisms of action as a basis for future nutritional claims related to both green and white teas. Green and white teas have a number of advantages that make them a very good alternative to other beverages which are widely consumed and less healthy. They are beverages with a pleasant flavor (flowers and fruit aroma with low levels of bitterness and astring ency) that are even commercialized flavored with other fruits and flowers. They are popular beverages, socially well accepted, economical, safe and consumed daily by hundreds of millions of people in the five
Score: 0.6372617483139038

Extracting passages from document: Green Tea -  Potential Health Benefits.pdf
Document: Green Tea -  Potential Health Benefits.pdf
Passage: caffeine (more than 300 mg per day) were compared with the effects on those who consumed small amounts of caffeine. There appeared to be no effect on the high consumers, but the low consumers regained sig- nificantly less weight (P < .01) than participants receiv - ing placebo.17 A 12-week double-blind controlled trial compared the effects of a green tea extract beverage high in catechins with a lower catechin placebo beverage in 240 Japanese adults who were obese.18 The results showed that the active treatment group had greater reductions in body weight, body mass index, body fat ratio, body fat mass, and waist and hip circumference ( P < .05).18 Cardiovas CUlar F UnCtion Epidemiologic studies suggest that green tea intake is associated with a reduced risk of cardiovascular disease, but the mechanisms remain uncertain. Clinical trials show inconsistent results in the effect of green tea on lipid levels, blood pressure, and coronary artery disease. A prospective cohort study of more than 40,000 Japanese adults found that green tea consumption was inversely associated with cardiovascular disease mor- tality.10 Women who consumed five or more cups per day had a 31 percent lower risk of dying from cardio - vascular disease.10 Participants who consumed five or more cups per day had a significantly reduced incidence of stroke.10sort : KEy rEComm Endations F or P raCtiCE Clinical recommendationEvidence rating References Ointment derived from green tea appears to be effective in the treatment of genital warts. B 4, 5
Score: 0.6759077906608582

Document: Green Tea -  Potential Health Benefits.pdf
Passage: to 0.97, and OR = 0.58; 95% CI, 0.34 to 0.90).11 Other studies have examined the relationship between green tea and prostate cancer. A small controlled trial followed 60 patients with high-grade prostate intraepi - thelial neoplasia.12 Patients were grouped randomly to receive green tea catechins extract (200 mg three times a day) or placebo for one year.12 Nine cancers were found in the placebo group, whereas only one cancer was detected in the green tea group.12 Another small clinical trial found no benefit from the use of green tea extract (500 mg per day for two to four months)13; however, a recent epidemiologic study of nearly 50,000 Japanese men found a dose-dependent relationship between green tea consumption and a reduction in the risk of advanced prostate cancer.14WEiGht mana GEmEnt Several small clinical trials have investigated the effect of green tea on weight loss and weight management.15,16 Some controlled trials suggest a benefit from green tea, whereas others do not. None of the studies demonstrate persistent effects. In one randomized placebo-controlled double-blind trial, investigators tracked the effects of green tea in 76 men and women who were overweight or obese.17 The effects of a green tea/caffeine mixture (two capsules, each containing 45 mg of EGCG and 25 mg of caffeine, taken before meals) on persons who habitually consumed large amounts of caffeine (more than 300 mg per day) were compared with the effects on those who consumed small amounts of caffeine. There appeared to be no
Score: 0.6609517335891724

``` 