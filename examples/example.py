import requests
import json
import base64

# Base URL of the Flask application
BASE_URL = "http://127.0.0.1:5000/correction/correct_sentence"
BASE_URL = "https://correctasentence.acecentre.net/correction/correct_sentence"

# Headers for the request
username = "azureUser"
password = "ACGpDyk8Wqb6YgVu3L2NBF"
encoded_credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
}

def correct_sentence(text, method="inbuilt"):
    """
    Send a request to the sentence correction API.

    Args:
    - text (str): The sentence to be corrected.
    - method (str): The correction method, either "inbuilt" or "gpt".
    """
    data = {
        "text": text,
        "correction_method": method,
        "correct_typos": True
    }

    response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print(f"Corrected Sentence ({method}):", response.json().get('corrected_sentence'))
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    # Example sentence to correct
    sentence = "Ths is a tst sentence with som errors."

    # Correct using the inbuilt method
    correct_sentence(sentence, "inbuilt")

    # Correct using the GPT method (ensure you have the correct authorization if needed)
    correct_sentence(sentence, "gpt")
