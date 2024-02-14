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


- We used Google Colab for preparing the data. Take a look [here](https://colab.research.google.com/drive/1VkKU9KKIWkWQZ-pPzdDFLeRnwFxdWUtq?usp=sharing) (a backup of the notebook is in this repo too)
- We then trained on a A100 lambdalabs machine which took around 3-6 hours. See Model-Train.pynb for details of what we used

#### The process to update the bigram/unigram list for wordsegment

See create_unigrams_spellingerrors.py and format_toefl.py

And also look at update_wordsegment.py

## Data Sources

This project leverages various datasets to train models and test the effectiveness of AAC-like corpora enhancements. Below are the primary sources of our data:

For a full model card see https://huggingface.co/willwade/t5-small-spoken-typo