import os
import json
import wordsegment
from collections import Counter
import random
import csv
import requests
from wordsegment import _segmenter
import re

def identity(value):
    return value


def readinbnc(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return text  # Return text directly

def tokenize(text):
    pattern = re.compile('[a-zA-Z]+')
    return [match.group(0) for match in pattern.finditer(text)]

def generate_bigrams(words):
    # Prepend <s> to indicate the start of a sentence
    words = ['<s>'] + words
    bigrams = zip(words, words[1:])
    return [' '.join(bigram) for bigram in bigrams]

def inject_typos(sentence, typo_dict, typo_probability=0.1):
    words = sentence.split()
    for i, word in enumerate(words):
        # Ensure there are typos available for the word and decide to inject a typo based on the given probability
        if word in typo_dict and typo_dict[word] and random.random() < typo_probability:
            # Replace the word with its typo version
            words[i] = random.choice(typo_dict[word])
    return ' '.join(words)


def process_sentences_from_csv(csv_file_path, typo_dict):
    all_bigrams = []  # Initialize a list to store all bigrams

    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for sentence in row:
                # Inject typos into the sentence
                sentence_with_typos = inject_typos(sentence, typo_dict)
                # Tokenize the sentence with injected typos
                tokenized_sentence = tokenize(sentence_with_typos)
                # Generate bigrams from the tokenized sentence
                bigrams = generate_bigrams(tokenized_sentence)
                # Append these bigrams to the all_bigrams list
                all_bigrams.extend(bigrams)

    # Now, update wordsegment.BIGRAMS with all collected bigrams
    # First, count the occurrences of each bigram
    bigram_counts = Counter(all_bigrams)

    # Then, update wordsegment.BIGRAMS with these counts
    for bigram, count in bigram_counts.items():
        if bigram in wordsegment.BIGRAMS:
            wordsegment.BIGRAMS[bigram] += count
        else:
            wordsegment.BIGRAMS[bigram] = count

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

def is_valid_word(word):
    # Check if the word is a single word without spaces and does not contain numbers
    return word.isalpha() and ' ' not in word


def process_spelling_file_to_typo_dict(file_path, output_file_path, typo_dict):
    with open(file_path, 'r') as file:
        correct_word = None
        for line in file:
            line = line.strip()
            if line.startswith('$'):
                # Extract the correct word, ensuring it's valid
                potential_correct_word = line[1:]
                if (potential_correct_word):
                    correct_word = potential_correct_word
                    if correct_word not in typo_dict:
                        typo_dict[correct_word] = []
                else:
                    correct_word = None  # Reset if not valid
            else:
                # Process only if we have a valid correct word and the misspelled word is valid
                if correct_word and is_valid_word(line):
                    typo_dict[correct_word].append(line)

    filtered_typo_dict = {word: typos for word, typos in typo_dict.items() if typos}
    typo_dict = filtered_typo_dict
    with open(output_file_path, 'w') as f:
        json.dump(typo_dict, f, indent=4)


def pairs(iterable):
    iterator = iter(iterable)
    values = [next(iterator)]
    for value in iterator:
        values.append(value)
        yield ' '.join(values)
        del values[0]

if __name__ == '__main__':
    # Load the standard corpus, clear and update unigrams and bigrams as before...
    # Process each spelling mistake file
    typo_dict = {}
    for filename in os.listdir('data/spelling-mistakes/'):
        if filename.endswith('.dat.txt'):
            file_path = os.path.join('data/spelling-mistakes/', filename)
            process_spelling_file_to_typo_dict(file_path, 'output/typo_dict.json', typo_dict)
    wordsegment.load()
    csv_file_path = 'output/processed_bnc2014.csv'
    text = readinbnc(csv_file_path)
    words = tokenize(text)
    wordsegment.UNIGRAMS.clear()
    wordsegment.UNIGRAMS.update(Counter(words))
    bigrams = generate_bigrams(words)  # Adjust this call as necessary
    wordsegment.BIGRAMS.clear()
    wordsegment.BIGRAMS.update(Counter(bigrams))
    # Now lets add typos
    # Do the same again but this time replacing 1 to 2 words with a found typo..
    process_sentences_from_csv(csv_file_path, typo_dict)
    
    # Continue with typo correction and processing...

    # Save the modified unigrams and bigrams for future use
    with open('modified_unigrams.json', 'w') as f:
        json.dump(wordsegment.UNIGRAMS, f)
    with open('modified_bigrams.json', 'w') as f:
        json.dump(wordsegment.BIGRAMS, f)

