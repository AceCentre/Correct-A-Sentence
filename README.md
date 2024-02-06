# Correct-A-Sentence

A really simple REST API to take a string which may have no spaces in it, find the word segments, correct it and then capitlaise it correctly

Note: We are using not just accurate spellings of words but a largish corpus of spelling mistakes too (see below for sources). This is probably making the word segmentation worse than better. Needs testing


NB: See swagger docs at http://correctasentence.acecentre.net

NOTE: to use gpt (which is using OpenAI GPt3.5Turbo-16K) you will need to provide a auth header like so

curl -X 'POST' \
  'http://127.0.0.1:5000/correction/correct_sentence' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -u 'azureUser:somepasswordhere-that-only-will-or-gavin-know' \
  -d '{
  "text": "ilikecheese",
  "correct_typos": true,
  "correction_method": "gpt"
}'


See also 
- https://github.com/willwade/dailyDialogCorrections/
- https://huggingface.co/willwade/t5-small-spoken-typo

All very WIP!

## Spelling Mistakes corpus

Directly from https://www.dcs.bbk.ac.uk/~ROGER/corpora.html

And https://github.com/EducationalTestingService/TOEFL-Spell/tree/master

