import sys
import argparse
import logging
import pyperclip
import time
import os
import requests
from requests.auth import HTTPBasicAuth
import base64
import json

if getattr(sys, 'frozen', False):
    # If the application is running as a PyInstaller bundle
    application_path = sys._MEIPASS
else:
    # If the application is running in a normal Python environment
    application_path = os.path.dirname(os.path.abspath(__file__))

# Setup logging
logging.basicConfig(filename=os.path.join(application_path, 'client.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_to_web(text, method="inbuilt"):
    """
    Send a request to the sentence correction API.

    Args:
    - text (str): The sentence to be corrected.
    - method (str): The correction method, either "inbuilt" or "gpt".
    """
    BASE_URL = "https://correctasentence.acecentre.net/correction/correct_sentence"
    username = '...'
    password = '...'
    encoded_credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
    }
    data = {
        "text": text,
        "correction_method": method,
        "correct_typos": True
    }

    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json().get('corrected_sentence', '')  # Return empty string if no corrected sentence is found
    except Exception as e:
        print(f"Error correcting sentence with {method}: {e}")
    return ''  # Return empty string in case of error or no response

def main():
    parser = argparse.ArgumentParser(description="Sentence Corrector Client")
    parser.add_argument("--sentence", type=str, help="Sentence to correct")
    parser.add_argument("--return", dest="return_string", action="store_true", help="Return the corrected sentence instead of copying to clipboard")
    args = parser.parse_args()

    sentence = args.sentence
    if not sentence:
        try:
            sentence = pyperclip.paste()
            if not isinstance(sentence, str) or not sentence.strip():
                logging.error("Clipboard does not contain valid text.")
                return
        except Exception as e:
            logging.error(f"Error reading from clipboard: {e}")
            return

    corrected_sentence = send_to_web(sentence,'gpt')
    if corrected_sentence:
        if args.return_string:
            print(corrected_sentence)
        else:
            try:
                pyperclip.copy(corrected_sentence)
            except Exception as e:
                logging.error(f"Error writing to clipboard: {e}")
    else:
        logging.error("Failed to correct the sentence due to an error with the sentence correction API.")

if __name__ == "__main__":
    main()
