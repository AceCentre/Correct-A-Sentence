import os
import re
import requests
import pandas as pd
from zipfile import ZipFile
from io import BytesIO
from happytransformer import HappyTextToText, TTSettings
# Constants
URL = "https://www.linguistics.ucsb.edu/sites/secure.lsit.ucsb.edu.ling.d7/files/sitefiles/research/SBC/SBCorpus.zip"
EXTRACT_DIR = "TRN"  # Initial extraction directory
TARGET_DIR = os.path.join(EXTRACT_DIR, "TRN")  # Adjusted to the nested TRN directory
# Initialize HappyTextToText with your chosen model
happy_tt = HappyTextToText("T5", "willwade/t5-small-spoken-typo")
args = TTSettings(num_beams=5, min_length=1)

def download_and_unzip(url, extract_to='TRN'):
    print(f"Downloading file from {url}")
    r = requests.get(url)
    z = ZipFile(BytesIO(r.content))
    print("Extracting files...")
    z.extractall(path=extract_to)
    print("Extraction completed.")

def clean_text(text):
    if text is None or text == '':
        return ''
    # Split the text to get the part after the third tab (if exists)
    parts = text.split('\t', 3)
    if len(parts) > 3:
        text = parts[3]
    else:
        return ''  # Return empty string if the text part doesn't exist
    
    # Apply cleaning operations
    text = re.sub(r'"', '', text)  # Remove speech marks
    text = re.sub(r'\%+', '', text)  # Remove percent signs and any consecutive percent signs
    text = re.sub(r'\[.*?\]|<.*?>', '', text)  # Remove content within square and angular brackets
    text = re.sub(r'\.\.+\s*', ' ', text)  # Remove sequences of two or more periods and any following space
    text = re.sub(r'=', '', text)  # Remove equal signs without replacement
    text = re.sub(r'@', '', text)  # Remove at symbols
    text = re.sub(r'~', '', text)  # Remove tilde symbols
    text = re.sub(r'-+', '', text)  # Remove dashes and replace with a space
    text = re.sub(r'\b[A-Z]+(?:\s+[A-Z]+)*:', '', text)  # Remove speaker labels
    text = re.sub(r'\(.*?\)', '', text)  # Remove text within parentheses and the parentheses themselves
    text = text.strip()
    return text



def grammar_correct(input_sentence):
    result = happy_tt.generate_text(f"grammar: {input_sentence}", args=args)
    return result.text

def process_files(directory):
    all_cleaned_lines = []  # List to store all cleaned lines across files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.trn'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    for line in file:
                        cleaned_line = clean_text(line)
                        if cleaned_line and len(cleaned_line.split()) > 1:
                            all_cleaned_lines.append(cleaned_line)
    
    # Create a DataFrame from the cleaned lines
    df = pd.DataFrame(all_cleaned_lines, columns=['Original'])
    
    # Apply grammar correction to each line
    df['Grammar-corrected'] = df['Original'].apply(grammar_correct)
    
    return df

if __name__ == "__main__":
    #download_and_unzip(URL)
    directory = "TRN/TRN"  # Adjust as necessary
    final_df = process_files(directory)
    # Save the final DataFrame to a CSV file
    final_df.to_csv("final_grammar_corrected.csv", index=False)
    