import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.metrics import accuracy_score

# Function to load a model and tokenizer with a specific commit
def load_model(model_name, revision):
    tokenizer = T5Tokenizer.from_pretrained(model_name, revision=revision)
    model = T5ForConditionalGeneration.from_pretrained(model_name, revision=revision)
    return tokenizer, model

# Function to correct grammar in a sentence
def correct_grammar(input_text, tokenizer, model):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    output = model.generate(input_ids, num_beams=5, min_length=1, max_new_tokens=50, early_stopping=True)
    decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
    return decoded_output

# Function to remove spaces from a sentence
def remove_spaces(text):
    return text.replace(" ", "")

# Updated function to evaluate a model specified by its commit hash
def evaluate_model(model_name, revision, test_data_path):
    tokenizer, model = load_model(model_name, revision)
    test_data = pd.read_csv(test_data_path)
    test_subset = pd.concat([test_data.head(100), test_data.tail(100)])
    #test_subset['input'] = test_subset['input'].apply(lambda x: remove_spaces(x))    

    predictions = []
    total = len(test_subset)
    print(f"Evaluating model {model_name}/{revision} on {total} sentences...")
    for index, row in test_subset.iterrows():
        corrected = correct_grammar(row['input'], tokenizer, model)
        predictions.append(corrected)
        # Print progress every 100 sentences
        if (index + 1) % 100 == 0 or index == total - 1:
            print(f"Processed {index + 1}/{total} sentences.")
            
    accuracy = accuracy_score(test_subset['target'].tolist(), predictions)
    print(f"Model {model_name}@{revision} Accuracy: {accuracy}\n")

# Example usage
model_name = 'willwade/t5-small-spoken-typo'  # Replace with your actual model name on Hugging Face
commits = ['73ff92ed563355fd83de4c9e20dddcf6f680fed2', '0a569d11998832bfbd01a91582be71edf4f328fd']  # Replace with your actual commit hashes
test_data_path = 'eval_data.csv'

for commit in commits:
    evaluate_model(model_name, commit, test_data_path)
