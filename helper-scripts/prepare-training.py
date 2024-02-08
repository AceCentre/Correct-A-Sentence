from tqdm import tqdm
from spellchecker import SpellChecker
import subprocess
import requests
import zipfile
import io
import os
import nltk
from nltk.tokenize import sent_tokenize
import random
import re
import xml.etree.ElementTree as ET
import csv
import glob

useaspell = False

def bnc_parse_xml_to_phrases_and_write_to_csv(xml_directory, output_csv='processed_bnc2014.csv'):
    xml_files = glob.glob(xml_directory + "*.xml")
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for xml_file in xml_files:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for utterance in root.findall(".//u"):
                text = ''.join(utterance.itertext())
                chunks = bnc_clean_and_chunk_utterance(text)
                for chunk in chunks:
                    csvwriter.writerow([chunk])

def bnc_clean_and_chunk_utterance(text):
    # Your existing logic to clean and chunk utterance text
    text = re.sub(r"<[^>]+>", "", text)
    chunks = re.split(r"\s*<pause dur=\"[^\"]+\"/>\s*", text)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip() and len(chunk.split()) > 1]
    return chunks


# Ensure NLTK punkt tokenizer is downloaded
nltk.download('punkt')

spell = SpellChecker()

# URLs for the typo data text files
typo_urls = [
    "https://www.dcs.bbk.ac.uk/~ROGER/missp.dat",
    "https://www.dcs.bbk.ac.uk/~ROGER/holbrook-missp.dat",
    "https://www.dcs.bbk.ac.uk/~ROGER/aspell.dat",
    "https://www.dcs.bbk.ac.uk/~ROGER/wikipedia.dat"
]

# URL for the spoken data
spoken_url = "https://aclanthology.org/attachments/I17-1099.Datasets.zip"
# URL of the homophones CSV file
homophones_url = "https://raw.githubusercontent.com/pimentel/homophones/master/homophones.csv"
# BNC URL - NOTE: You get this after you sign the licence http://corpora.lancs.ac.uk/bnc2014/licence.php
bnc_dir = "bnc2014spoken-xml"


def parse_homophones_from_file(filepath):
    """
    Parse the CSV content of homophones from a file and return a list of homophone sets.
    
    :param filepath: Path to the homophones CSV file.
    :return: A list of lists, where each sublist contains words that are homophones.
    """
    homophones = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            homophones.append(row)
    return homophones


def replace_homophones(sentence, homophones, homonym_rate=0.05):
    words = sentence.split()
    new_sentence = []
    for word in words:
        if random.random() < homonym_rate:  # Only replace at the specified rate
            homophone_set = [homophone_list for homophone_list in homophones if word.lower() in homophone_list]
            if homophone_set:
                replacement_options = [homophone for homophone in homophone_set[0] if homophone.lower() != word.lower() and is_valid_word(homophone)]
                if replacement_options:
                    new_word = random.choice(replacement_options)
                    new_sentence.append(new_word)
                    continue
        new_sentence.append(word)
    return ' '.join(new_sentence)


def apply_typo_dictionary(sentence, typo_dict):
    words = sentence.split()
    new_sentence = []
    for word in words:
        # Check if the word has known typos and select only valid ones
        if word.lower() in typo_dict:
            valid_typos = [typo for typo in typo_dict[word.lower()] if is_valid_word(typo)]
            if valid_typos and random.random() < 0.1:  # Adjust the probability as needed
                typo = random.choice(valid_typos)
                new_sentence.append(typo)
            else:
                new_sentence.append(word)
        else:
            new_sentence.append(word)
    return ' '.join(new_sentence)

    
def augment_dataset(sentences, homophones, typo_dict, file_name, typo_rate=0.05):  # Adjust typo_rate here
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["input", "target"])
        
        for original_sentence in tqdm(sentences, desc="Augmenting Sentences"):
            # Clean original sentence (e.g., remove "mm")
            clean_sentence = re.sub(r'\bmm\b', '', original_sentence)  # \b denotes word boundary
            clean_sentence = re.sub(r'\s+', ' ', clean_sentence).strip()  # Replace one or more spaces with a single space
            clean_sentence = clean_sentence.replace("_", " ").replace("  ", " ").strip()

            
            # Apply calculated typos
            typo_sentence = introduce_typos(clean_sentence, typo_rate)
            
            # Apply homonym replacement
            homonym_sentence = replace_homophones(typo_sentence, homophones, homonym_rate=0.05)  # Adjust the rate as needed
            
            # Apply typo dictionary lookup and replacement
            final_bad_sentence = apply_typo_dictionary(homonym_sentence, typo_dict).replace("_", " ")
            final_bad_sentence = final_bad_sentence.replace("'", "")
            #lastly lets just double make sure a change does occur
            final_bad_sentence = ensure_modification(clean_sentence, final_bad_sentence, homophones, typo_dict)
            
            
            # Contracted version (no spaces)
            contracted_bad_sentence = final_bad_sentence.replace(" ", "")
            
            # Check sentence length (in words) and ignore if not within 2-5 words
            if 2 <= len(clean_sentence.split()) <= 5:
                # Write both original and final "bad" sentence to the CSV file
                writer.writerow([final_bad_sentence, clean_sentence])  # Regular spacing
                writer.writerow([contracted_bad_sentence, clean_sentence])  # Contracted version


keyboard_layout = {
    'a': ['q', 'w', 's', 'z'],
    'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 'r', 'd', 's'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'o', 'k', 'j'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k', 'l'],
    'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'p', 'l', 'k'],
    'p': ['o', 'l'],
    'q': ['w', 'a'],
    'r': ['e', 't', 'f', 'd'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'y', 'g', 'f'],
    'u': ['y', 'i', 'j', 'h'],
    'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'e', 's', 'a'],
    'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'u', 'h', 'g'],
    'z': ['a', 's', 'x'],
}

def introduce_typos(sentence, typo_rate=0.1, max_typos=2):
    """Introduce advanced typos into a sentence, excluding numbers, with a limit on the number of typos."""
    new_sentence = []
    words = sentence.split()
    typos_introduced = 0

    for word in words:
        if random.random() < typo_rate and typos_introduced < max_typos:
            typo_type = random.choice(['substitution', 'deletion', 'insertion', 'transposition', 'repeated_letters'])
            modified_word = word  # Default to the original word

            if typo_type == 'substitution' and len(word) > 1:
                idx = random.randint(0, len(word) - 1)
                substitute_char = random.choice(keyboard_layout.get(word[idx], [c for c in string.ascii_lowercase if c != word[idx]]))
                modified_word = word[:idx] + substitute_char + word[idx+1:]

            elif typo_type == 'insertion':
                idx = random.randint(0, len(word) - 1)
                insert_char = random.choice([c for c in string.ascii_lowercase])  # Explicitly exclude digits
                modified_word = word[:idx] + insert_char + word[idx:]

            elif typo_type == 'deletion' and len(word) > 1:
                idx = random.randint(0, len(word) - 1)
                modified_word = word[:idx] + word[idx+1:]

            elif typo_type == 'transposition' and len(word) > 1:
                idx = random.randint(0, len(word) - 2)
                modified_word = word[:idx] + word[idx+1] + word[idx] + word[idx+2:]

            elif typo_type == 'repeated_letters' and len(word) > 1:
                idx = random.randint(0, len(word) - 1)
                modified_word = word[:idx] + word[idx] + word[idx] + word[idx+1:]

            # Only count as a typo if the word was modified
            if modified_word != word:
                typos_introduced += 1
                new_sentence.append(modified_word)
            else:
                new_sentence.append(word)
        else:
            new_sentence.append(word)

    return " ".join(new_sentence)
    
def is_valid_word(word):
    """Check if the word is valid (contains only letters)."""
    return re.match("^[a-zA-Z]+$", word) is not None
    
    
def phonetic_replacement(word):
    replacements = {
    'c': ['k', 's'],
    'q': ['k', 'cu'],
    'x': ['ks', 'z'],
    'ph': ['f'],
    'gh': ['g', 'f'],
    'ough': ['uff', 'off', 'ow'],
    'ea': ['ee', 'ie'],
    'ie': ['ei', 'ee'],
    'ai': ['ei', 'ay'],
    'ay': ['ai', 'ei'],
    'ou': ['ow', 'oo'],
    'ow': ['ou', 'oo'],
    'th': ['t', 'f'],
    'ee': ['ie', 'ea'],
    'oo': ['u', 'ou'],
    'ck': ['k', 'c'],
    'ch': ['k', 'sh'],
    'sh': ['ch', 's'],
    'tch': ['ch', 't'],
    'dge': ['g', 'j'],
    'ture': ['cher'],
    'ight': ['ite', 'ight'],
    'y': ['i', 'ie'],
    'eigh': ['ay', 'ai'],
    'au': ['aw', 'o'],
    'aw': ['au', 'o'],
    'ue': ['u', 'ew'],
    'ew': ['u', 'ue'],
    'ar': ['er', 'or'],
    'er': ['ar', 'or'],
    'or': ['ar', 'er']    }
    for original, possible_replacements in replacements.items():
        if original in word:
            replacement = random.choice(possible_replacements)
            word = word.replace(original, replacement, 1)  # Replace only the first occurrence
            break  # Stop after the first replacement to avoid over-modification
    return word


spell_check_cache = {}

def is_correct_spelling(word):
    if useaspell:
        if word in spell_check_cache:
            return spell_check_cache[word]
        result = subprocess.run(['aspell', 'list'], input=word, text=True, capture_output=True)
        is_correct = result.stdout == ""
        spell_check_cache[word] = is_correct
        return is_correct
    else:
        return word in spell
    
# Function to download and process typo data
def download_and_process_typo_data(urls):
    for url in urls:
        filename = url.split('/')[-1]  # Extract filename from URL
        local_path = f"spelling-mistakes/{filename}"  # Define local path to save file

        # Check if the file already exists to avoid re-downloading
        if not os.path.exists(local_path):
            print(f"Downloading data from {url}")
            response = requests.get(url)  # This line defines 'response'
            # Ensure the request was successful
            response.raise_for_status()

            # Save the response content to a file
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"Finished downloading data from {url}")
        else:
            print(f"File {filename} already exists. Skipping download.")

        # Process the downloaded file
        with open(local_path, 'r', encoding='utf-8') as f:
            response_text = f.read()  # Read the content of the file

        # Your existing logic to process 'response_text'
        lines = response_text.split('\n')
        correct_word = None
        for line in lines:
            if line.startswith('$'):
                correct_word = line[1:]
            elif correct_word:
                # Your logic to check spelling and write to CSV
                pass

# Function to introduce typos into a sentence
def introduce_typos(sentence, typo_rate=0.1):
    new_sentence = ""
    for word in sentence.split():
        if random.random() < typo_rate:
            typo_type = random.choice(['swap', 'miss', 'add', 'wrong'])
            if typo_type == 'swap' and len(word) > 1:
                idx = random.randint(0, len(word) - 2)
                word = word[:idx] + word[idx+1] + word[idx] + word[idx+2:]
            elif typo_type == 'miss' and len(word) > 1:
                idx = random.randint(0, len(word) - 1)
                word = word[:idx] + word[idx+1:]
            elif typo_type == 'add':
                idx = random.randint(0, len(word) - 1)
                word = word[:idx] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[idx:]
            elif typo_type == 'wrong' and len(word) > 1:
                idx = random.randint(0, len(word) - 1)
                word = word[:idx] + random.choice('abcdefghijklmnopqrstuvwxyz') + word[idx+1:]
        new_sentence += word + " "
    return new_sentence.strip()

# Function to clean punctuation spacing
def clean_punctuation_spacing(sentence):
    sentence = re.sub(r"\s+’\s+", "’", sentence)
    sentence = re.sub(r"\s+'\s+", "'", sentence)
    sentence = re.sub(r"\s+\?", "?", sentence)
    sentence = re.sub(r"\s+\.", ".", sentence)
    sentence = re.sub(r"\s+!", "!", sentence)
    sentence = re.sub(r"\s+,", ",", sentence)
    sentence = re.sub(r"\s+;", ";", sentence)
    sentence = re.sub(r"\s+:", ":", sentence)
    return sentence

# Function to process dialogues from a file and save to CSV
def process_and_save_spoken_data():
    file_path = 'EMNLP_dataset/EMNLP_dataset/dialogues_text.txt'  # Adjust path as necessary
    data_pairs = process_dialogues_file(file_path)
    save_to_csv(data_pairs)

def clean_input(sentence):
    """Clean the input sentence by removing specific characters."""
    sentence = sentence.replace("’", "")  # Remove apostrophes
    sentence = sentence.replace(".", "")  # Remove periods
    return sentence

def process_dialogues(text):
    """Process dialogues to create a dataset for text correction with updated requirements."""
    sentences = sent_tokenize(text)
    data_pairs = []
    for sentence in sentences:
        # Remove lines enclosed in quotation marks and ensure word count is within limits
        if sentence.startswith('"') and sentence.endswith('"'):
            sentence = sentence[1:-1]
        word_count = len(sentence.split())
        if 2 <= word_count <= 5:
            cleaned_sentence = clean_punctuation_spacing(sentence)
            typo_sentence = introduce_typos(clean_input(cleaned_sentence), typo_rate=0.1)
            data_pairs.append({"input": typo_sentence, "target": cleaned_sentence})
    return data_pairs


def process_dialogues_file(file_path):
    """Read dialogues from a file, process them, and return data pairs."""
    data_pairs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        dialogues = text.split('__eou__')
        for dialogue in dialogues:
            if dialogue.strip():  # Check if dialogue is not just whitespace
                data_pairs.extend(process_dialogues(dialogue.strip()))
    return data_pairs

def save_to_csv(data_pairs, output_file='processed_dialogues.csv'):
    """Save processed data pairs to a CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["input", "target"])
        writer.writeheader()
        for pair in data_pairs:
            writer.writerow(pair)
            

def load_typo_data_into_dict(urls):
    typo_dict = {}
    for url in urls:
        response = requests.get(url)
        lines = response.text.split('\n')
        for line in lines:
            if line.startswith('$'):
                correct_word = line[1:]
            else:
                if correct_word in typo_dict:
                    typo_dict[correct_word].append(line)
                else:
                    typo_dict[correct_word] = [line]
    return typo_dict

def load_spoken_data_into_list(file_path):
    spoken_sentences = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            processed_line = line.strip()
            spoken_sentences.append(processed_line)
    return spoken_sentences

def read_sentences_from_csv(csv_file='processed_bnc2014.csv'):
    sentences = []
    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader, None)  # Skip the header
        for row in csvreader:
            if row:  # Check if row is not empty
                sentences.append(row[0])  # Assuming the sentence is in the first column
    return sentences
    
    
def download_file_if_not_exists(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename}...")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
    else:
        print(f"{filename} already exists. Skipping download.")

def download_and_unzip_spoken_data_if_needed(url, extract_to_dir):
    if not os.path.exists(extract_to_dir) or not os.listdir(extract_to_dir):
        print(f"Downloading and extracting spoken data to {extract_to_dir}...")
        response = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(extract_to_dir)
    else:
        print(f"Spoken data already exists in {extract_to_dir}. Skipping download and extraction.")

def ensure_modification(original_sentence, modified_sentence, homophones, typo_dict):
    if original_sentence == modified_sentence:
        # Force a modification if none has occurred
        modified_sentence = force_change(modified_sentence, homophones, typo_dict)
    return modified_sentence

def force_change(sentence, homophones, typo_dict, typo_preference=0.8):
    """Force a change in the sentence with a preference for typos over homophones."""
    words = sentence.split()
    new_sentence = []

    for i, word in enumerate(words):
        if random.random() < typo_preference and word.lower() in typo_dict:
            # Apply a typo with higher preference
            new_word = random.choice(typo_dict[word.lower()])
            new_sentence.append(new_word)
        else:
            # Attempt to apply a homophone change
            homophone_list = next((h for h in homophones if word.lower() in h), None)
            if homophone_list:
                choices = [h for h in homophone_list if h.lower() != word.lower() and is_valid_word(h)]
                if choices:
                    new_word = random.choice(choices)
                    new_sentence.append(new_word)
                else:
                    new_sentence.append(word)  # No suitable homophone found, keep original
            else:
                new_sentence.append(word)  # No homophone or typo applicable, keep original

    return " ".join(new_sentence)


    
# Assuming BNC data is now in the specified directory
print('starting bnc')
bnc_dir = "bnc2014spoken-xml"
bnc_parse_xml_to_phrases_and_write_to_csv(bnc_dir + "/spoken/untagged/")
print('bnc done')
# Process homophones
homophones_filename = homophones_url.split('/')[-1]
download_file_if_not_exists(homophones_url, f"{homophones_filename}")
homophones = parse_homophones_from_file(homophones_filename)
print('homophone done')
# Download and process typo data, spoken data, and then augment and process BNC data
download_and_process_typo_data(typo_urls)
print('typo download done')
typo_dict = load_typo_data_into_dict(typo_urls)
print('loaded typo')
download_and_unzip_spoken_data_if_needed(spoken_url,'./')
print('download spoken')
process_and_save_spoken_data()
print('save spoken')

spoken_sentences = load_spoken_data_into_list('EMNLP_dataset/EMNLP_dataset/dialogues_text.txt')
print('spoken sentences done')
bnc_sentences = read_sentences_from_csv('processed_bnc2014.csv')
spoken_sentences.extend(bnc_sentences)  # Combine BNC sentences with spoken dataset sentences

# Assuming BNC data is now in bnc_dataset directory
augmented_bnc = augment_dataset(bnc_sentences, homophones, typo_dict,'data_augment.csv')


print("All data processed and saved.")
