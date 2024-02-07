# Spoken "AAC-Like" corpora 

So you can 

``python
pip install -r requirements.txt
``
then

Download the [BNC Corpora 2014](http://corpora.lancs.ac.uk/bnc2014/signup.php)

Unzip. It should be in a directory like `bnc2014spoken-xml` in the same as the script

tnen

``python

python prepare-training.python
``

## What does it do?

- Takes the data from Daily Dialog and BNC Corpora 2014
- Adds homonym changes
- Adds typo changes - both at a rate of around 0.05%
- Only picks lines of 2-5 words long
- Then makes a training file with these sentences and compressed (no spaces) sentences



## Datasets for spoken:

- [DailyDialog](https://aclanthology.org/I17-1099/)
- [BNC Corpora 2014](http://corpora.lancs.ac.uk/bnc2014/signup.php)

## Datasets for spelling mistakes:

- [TOEFL Spell, Birkbeck etc](https://www.dcs.bbk.ac.uk/~ROGER/corpora.html)


See then our parser scripts to clean this data for our use. 

