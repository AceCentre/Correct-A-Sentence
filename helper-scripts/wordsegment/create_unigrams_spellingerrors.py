import os
import json
import wordsegment
from collections import Counter

# Load the standard corpus
wordsegment.load()

# Function to process a single spelling mistake file
def process_spelling_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('$'):
                correct_word = line[1:]
                correct_word_weight = wordsegment.UNIGRAMS.get(correct_word, 0)
            else:
                misspelled_word = line
                # Assign the weight of the correct word to the misspelled word
                wordsegment.UNIGRAMS[misspelled_word] = correct_word_weight

# Directory containing the spelling mistake files
spelling_mistakes_dir = 'data/spelling-mistakes'

# Process each spelling mistake file
for filename in os.listdir(spelling_mistakes_dir):
    if filename.endswith('.dat.txt'):
        file_path = os.path.join(spelling_mistakes_dir, filename)
        process_spelling_file(file_path)

# Save the modified unigrams and bigrams for future use
with open('modified_unigrams.json', 'w') as f:
    json.dump(wordsegment.UNIGRAMS, f)
with open('modified_bigrams.json', 'w') as f:
    json.dump(wordsegment.BIGRAMS, f)
