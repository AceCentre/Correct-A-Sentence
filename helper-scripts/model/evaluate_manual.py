import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
import Levenshtein

# Function to load a model and tokenizer with a specific commit
def load_model(model_name, revision):
    tokenizer = T5Tokenizer.from_pretrained(model_name, revision=revision)
    model = T5ForConditionalGeneration.from_pretrained(model_name, revision=revision)
    return tokenizer, model

# Function to preprocess text by removing spaces
def remove_spaces(text):
    return text.replace(" ", "")

# Function to calculate similarity using Levenshtein distance
def calculate_similarity(corrected_sentence, correct_sentence):
    corrected_sentence = corrected_sentence or ''
    correct_sentence = correct_sentence or ''
    distance = Levenshtein.distance(corrected_sentence.lower(), correct_sentence.lower())
    max_len = max(len(corrected_sentence), len(correct_sentence))
    similarity = 1 - (distance / max_len) if max_len else 1
    return similarity

# Updated function to evaluate a model specified by its commit hash on a subset of data
def evaluate_model(model_name, revision, test_data_path):
    tokenizer, model = load_model(model_name, revision)
    test_data = pd.read_csv(test_data_path)
    test_subset = pd.concat([test_data.head(100), test_data.tail(100)])
    #test_subset['input'] = test_subset['input'].apply(remove_spaces)

    predictions = []
    similarities = []
    total = len(test_subset)
    print(f"Evaluating model {model_name}@{revision} on {total} sentences...")
    
    for _, row in test_subset.iterrows():
        corrected = correct_grammar(row['input'], tokenizer, model)
        similarity = calculate_similarity(corrected, row['target'])
        similarities.append(similarity)
    
    average_similarity = sum(similarities) / len(similarities)
    print(f"Model {model_name}@{revision} Average Similarity: {average_similarity:.3f}")

# Function to correct grammar in a sentence
def correct_grammar(input_text, tokenizer, model):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(input_ids, num_beams=5, min_length=1, max_length=512, early_stopping=True)
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded_output

# Example usage
model_name = 'willwade/t5-small-spoken-typo'
commits = ['73ff92ed563355fd83de4c9e20dddcf6f680fed2', '0a569d11998832bfbd01a91582be71edf4f328fd']
test_data_path = 'test_data.csv'

for commit in commits:
    evaluate_model(model_name, commit, test_data_path)
