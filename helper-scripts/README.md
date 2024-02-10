# Spoken "AAC-Like" Corpora Enhancement

## Overview

This project aims to enhance prediction accuracy and address common typographical errors in Augmentative and Alternative Communication (AAC) systems. It focuses on improving the handling of:
- Homonyms
- Typographical errors (Typos++)
- Writing without spaces

To achieve these goals, we employ two main techniques to attempt this:
1. **Word Segmentation**: Utilizing `wordsegment`. We update the bigram and unigram lists for better handling of texts written without spaces.
2. **Language Model Training**: Leveraging `Happy Transformers` with a base T5 model designed to correct grammar errors.
3. (**LLM** GPT3.5 Does a fine job. But we want it working offline)

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system. You will also need `pip` for installing Python packages.

### Installation

#### The prepare script for our Transfomer fine tuned training

1. Clone the repository or download the source code.
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Download the [BNC Corpora 2014](http://corpora.lancs.ac.uk/bnc2014/signup.php) and unzip it. Ensure the unzipped directory bnc2014spoken-xml is located in the same directory as the script.

### Usage

```python
python prepare-training.py
```

This script performs the following operations:

- Processes data from the Daily Dialog and BNC Corpora 2014.
- Introduces homonym and typo changes at a rate of approximately 0.05%.
- Filters sentences to only include those with 2-5 words.
- Generates a training file with these sentences and their compressed (no spaces) counterparts.

#### The process to update the bigram/unigram list for wordsegment

See create_unigrams_spellingerrors.py

If I'm honest this needs more work


## Data Sources

This project leverages various datasets to train models and test the effectiveness of AAC-like corpora enhancements. Below are the primary sources of our data:

### Datasets for Spoken Language:

- **DailyDialog**: A high-quality multi-turn dialog dataset that covers various topics in our daily life. It is useful for training models to understand and generate human-like conversational texts.
  - Access it [here](https://aclanthology.org/I17-1099/).

- **BNC Corpora 2014**: The British National Corpus (BNC) 2014 is a large, diverse collection of spoken and written texts in British English from the late twentieth century.
  - Sign up and download [here](http://corpora.lancs.ac.uk/bnc2014/signup.php).

### Datasets for Spelling Mistakes:

- **Typo lists, Birkbeck, etc.**: These datasets contain lists of commonly misspelled words, making them invaluable for training models to recognize and correct spelling errors.
  - Find these resources [here](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html).
- **TOEFL Spell** A dataset of Spelling Annotations for English language learner essays written for TOEFL exams.
  - Find this [here](https://github.com/EducationalTestingService/TOEFL-Spell/tree/master) 

Each dataset plays a crucial role in developing and refining the techniques used in this project to improve AAC systems' accuracy and usability. By incorporating real-world data from spoken dialogues and common spelling mistakes, we aim to create more robust and effective solutions for AAC users.
