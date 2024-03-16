import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sklearn.metrics import accuracy_score

# Function to load a model and tokenizer
def load_model(model_dir):
    tokenizer = T5Tokenizer.from_pretrained(model_dir)
    model = T5ForConditionalGeneration.from_pretrained(model_dir)
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


# Function to evaluate a model with progress updates
def evaluate_model(model_dir, test_data_path):
    tokenizer, model = load_model(model_dir)
    test_data = pd.read_csv(test_data_path)
    test_subset = pd.concat([test_data.head(100), test_data.tail(100)])
    test_subset['input'] = test_subset['input'].apply(lambda x: remove_spaces(x))

    
    predictions = []
    total = len(test_subset)
    print(f"Evaluating model {model_dir} on {total} sentences...")
    for index, row in test_subset.iterrows():
        corrected = correct_grammar(row['input'], tokenizer, model)
        predictions.append(corrected)
        
        # Print progress every 100 sentences
        if (index + 1) % 100 == 0 or index == total - 1:
            print(f"Processed {index + 1}/{total} sentences.")
    
    accuracy = accuracy_score(test_subset['target'].tolist(), predictions)
    print(f"Model {model_dir} Accuracy: {accuracy}\n")

# Paths to your fine-tuned models and test dataset
model_dirs = ['finetuned-model', 'finetuned-model-continued']
test_data_path = 'test_data.csv'
evaluate_model('t5-small-spoken-typo-new', test_data_path)
#for model_dir in model_dirs:
#    evaluate_model(model_dir, test_data_path)
