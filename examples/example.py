import requests
import json
import base64
import csv
from happytransformer import HappyTextToText, TTSettings
import Levenshtein
import time

# Initialize HappyTransformer
happy_tt = HappyTextToText("T5", "./t5-small-spoken-typo")
args = TTSettings(num_beams=5, min_length=1)
# And base
happy_ttbase = HappyTextToText("T5", "vennify/t5-base-grammar-correction")
happy_ttt5 = HappyTextToText("T5", "t5-small")
happy_c4small = HappyTextToText("T5", "visheratin/t5-efficient-mini-grammar-correction")
happy_will = HappyTextToText("T5", "./t5-small-spoken-typo")

# Base URL of the Flask application
BASE_URL = "https://correctasentence.acecentre.net/correction/correct_sentence"

# Headers for the request
username = "azureUser"
password = "ACGpDyk8Wqb6YgVu3L2NBF"
encoded_credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {encoded_credentials}"
}

def calculate_similarity(corrected_sentence, correct_sentence):
    """
    Calculate the similarity between two sentences using Levenshtein distance.

    Args:
    - corrected_sentence (str): The corrected sentence.
    - correct_sentence (str): The correct sentence.

    Returns:
    - similarity (float): The similarity score, normalized to be between 0 and 1.
    """
    # Handle None inputs by treating them as empty strings
    corrected_sentence = corrected_sentence or ''
    correct_sentence = correct_sentence or ''

    distance = Levenshtein.distance(corrected_sentence.lower(), correct_sentence.lower())
    max_len = max(len(corrected_sentence), len(correct_sentence))
    similarity = 1 - (distance / max_len) if max_len else 1
    return similarity

def correct_sentence_api(text, method="inbuilt"):
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

    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json().get('corrected_sentence', '')  # Return empty string if no corrected sentence is found
    except Exception as e:
        print(f"Error correcting sentence with {method}: {e}")
    return ''  # Return empty string in case of error or no response

def correct_sentence_happy(text):
    """
    Correct a sentence using HappyTransformer.

    Args:
    - text (str): The sentence to be corrected.
    """
    try:
        result = happy_tt.generate_text(f"grammar: {text}", args=args)
        corrected_sentence = result.text.replace("grammar: ", "").strip("[]").strip("'\" ")
        return corrected_sentence
    except Exception as e:
        print(f"Error correcting sentence with HappyTransformer: {e}")
        return ''  # Return empty string in case of error

def correct_sentence_happybase(text):
    """
    Correct a sentence using HappyTransformer.

    Args:
    - text (str): The sentence to be corrected.
    """
    try:
        result = happy_ttbase.generate_text(f"grammar: {text}", args=args)
        corrected_sentence = result.text.replace("grammar: ", "").strip("[]").strip("'\" ")
        return corrected_sentence
    except Exception as e:
        print(f"Error correcting sentence with HappyTransformer: {e}")
        return ''  # Return empty string in case of error

def correct_sentence_happyt5(text):
    """
    Correct a sentence using HappyTransformer.

    Args:
    - text (str): The sentence to be corrected.
    """
    try:
        result = happy_ttt5.generate_text(f"grammar: {text}", args=args)
        corrected_sentence = result.text.replace("grammar: ", "").strip("[]").strip("'\" ")
        return corrected_sentence
    except Exception as e:
        print(f"Error correcting sentence with HappyTransformer: {e}")
        return ''  # Return empty string in case of error

def correct_sentence_happyc4small(text):
    """
    Correct a sentence using HappyTransformer.

    Args:
    - text (str): The sentence to be corrected.
    """
    try:
        result = happy_c4small.generate_text(f"{text}", args=args)
        corrected_sentence = result.text.replace("grammar: ", "").strip("[]").strip("'\" ")
        return corrected_sentence
    except Exception as e:
        print(f"Error correcting sentence with HappyTransformer: {e}")
        return ''  # Return empty string in case of error

def correct_sentence_happywill(text):
    """
    Correct a sentence using HappyTransformer.

    Args:
    - text (str): The sentence to be corrected.
    """
    try:
        result = happy_will.generate_text(f"grammar: {text}", args=args)
        corrected_sentence = result.text.replace("grammar: ", "").strip("[]").strip("'\" ")
        return corrected_sentence
    except Exception as e:
        print(f"Error correcting sentence with HappyTransformer: {e}")
        return ''  # Return empty string in case of error


def calculate_accuracy(corrected_sentences, correct_answers):
    # Ensure both lists have the same length
    assert len(corrected_sentences) == len(correct_answers), "Lists of corrected sentences and correct answers must have the same length."

    # Filter out None values and calculate accuracy
    filtered_pairs = [(corrected, correct) for corrected, correct in zip(corrected_sentences, correct_answers) if corrected is not None]
    correct_count = sum(1 for corrected, correct in filtered_pairs if corrected.lower() == correct.lower())
    return correct_count / len(filtered_pairs) * 100 if filtered_pairs else 0

if __name__ == "__main__":
    corrected_sentences_inbuilt = []
    corrected_sentences_gpt = []
    corrected_sentences_happy = []
    corrected_sentences_happybase = []
    corrected_sentences_happyt5 = []
    corrected_sentences_happyc4small = []
    corrected_sentences_happyc4small = []
    corrected_sentences_happywill = []
    correct_answers = []
    incorrect_strings = []

    with open("examplestrings.csv", "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header if present
        for row in reader:
            incorrect_sentence, correct_sentence = row
            correct_answers.append(correct_sentence.strip())
            incorrect_strings.append(incorrect_sentence.strip())
    
            start_time = time.time()
            corrected_inbuilt = correct_sentence_api(incorrect_sentence, "inbuilt")
            inbuilt_time = time.time() - start_time
            inbuilt_similarity = calculate_similarity(corrected_inbuilt, correct_sentence)
            corrected_sentences_inbuilt.append((corrected_inbuilt, inbuilt_time, inbuilt_similarity))

            # Correct using the GPT method
            start_time = time.time()
            corrected_gpt = correct_sentence_api(incorrect_sentence, "gpt")
            gpt_time = time.time() - start_time
            gpt_similarity = calculate_similarity(corrected_gpt, correct_sentence)
            corrected_sentences_gpt.append((corrected_gpt, gpt_time, gpt_similarity))

            # Correct using HappyTransformer
            start_time = time.time()
            corrected_happy = correct_sentence_happy(incorrect_sentence)
            happy_time = time.time() - start_time
            happy_similarity = calculate_similarity(corrected_happy, correct_sentence)
            corrected_sentences_happy.append((corrected_happy, happy_time, happy_similarity))


            # Correct using HappyTransformer -base
            start_time = time.time()
            corrected_happybase = correct_sentence_happybase(incorrect_sentence)
            happybase_time = time.time() - start_time
            happybase_similarity = calculate_similarity(corrected_happybase, correct_sentence)
            corrected_sentences_happybase.append((corrected_happybase, happybase_time, happybase_similarity))


            # Correct using HappyTransformer -t5small
            start_time = time.time()
            corrected_happyt5 = correct_sentence_happyt5(incorrect_sentence)
            happyt5_time = time.time() - start_time
            happyt5_similarity = calculate_similarity(corrected_happyt5, correct_sentence)
            corrected_sentences_happyt5.append((corrected_happyt5, happyt5_time, happyt5_similarity))

            # Correct using HappyTransformer -c4small
            start_time = time.time()
            corrected_happyc4small = correct_sentence_happyc4small(incorrect_sentence)
            happyc4small_time = time.time() - start_time
            happyc4small_similarity = calculate_similarity(corrected_happyc4small, correct_sentence)
            corrected_sentences_happyc4small.append((corrected_happyc4small, happyc4small_time, happyc4small_similarity))

            start_time = time.time()
            corrected_happywill = correct_sentence_happywill(incorrect_sentence)
            happywill_time = time.time() - start_time
            happywill_similarity = calculate_similarity(corrected_happywill, correct_sentence)
            corrected_sentences_happywill.append((corrected_happywill, happywill_time, happywill_similarity))

    # Calculate accuracy
    corrected_sentences_inbuilt_only = [corrected for corrected, _, _ in corrected_sentences_inbuilt]
    corrected_sentences_gpt_only = [corrected for corrected, _, _ in corrected_sentences_gpt]
    corrected_sentences_happy_only = [corrected for corrected, _, _ in corrected_sentences_happy]
    corrected_sentences_happybase_only = [corrected for corrected, _, _ in corrected_sentences_happybase]
    corrected_sentences_happyt5_only = [corrected for corrected, _, _ in corrected_sentences_happyt5]
    corrected_sentences_happyc4small_only = [corrected for corrected, _, _ in corrected_sentences_happyc4small]
    corrected_sentences_happywill_only = [corrected for corrected, _, _ in corrected_sentences_happywill]

    # Calculate accuracy
    accuracy_inbuilt = calculate_accuracy(corrected_sentences_inbuilt_only, correct_answers)
    accuracy_gpt = calculate_accuracy(corrected_sentences_gpt_only, correct_answers)
    accuracy_happy = calculate_accuracy(corrected_sentences_happy_only, correct_answers)
    accuracy_happybase = calculate_accuracy(corrected_sentences_happybase_only, correct_answers)
    accuracy_happyt5 = calculate_accuracy(corrected_sentences_happyt5_only, correct_answers)
    accuracy_happyc4small = calculate_accuracy(corrected_sentences_happyc4small_only, correct_answers)
    accuracy_happywill = calculate_accuracy(corrected_sentences_happywill_only, correct_answers)

    print(f"Accuracy of inbuilt method: {accuracy_inbuilt}%")
    print(f"Accuracy of GPT method: {accuracy_gpt}%")
    print(f"Accuracy of Happy method: {accuracy_happy}%")
    print(f"Accuracy of Happy Base method: {accuracy_happybase}%")
    print(f"Accuracy of Happy T5 small method: {accuracy_happyt5}%")
    print(f"Accuracy of Happy C4 small method: {accuracy_happyc4small}%")
    print(f"Accuracy of Happy Will small method: {accuracy_happywill}%")
    
    #for method_name, results in [("inbuilt", corrected_sentences_inbuilt), ("GPT", corrected_sentences_gpt), ("Happy", corrected_sentences_happy)]:
    for method_name, results in [("inbuilt", corrected_sentences_inbuilt), ("GPT", corrected_sentences_gpt), ("Happy", corrected_sentences_happy), ("HappyC4Small", corrected_sentences_happyc4small), ("HappyWill", corrected_sentences_happywill)]:
        total_time = sum(time for _, time, _ in results)
        average_similarity = sum(similarity for _, _, similarity in results) / len(results)
        print(f"{method_name} method - Total time: {total_time:.2f} seconds, Average similarity: {average_similarity:.2f}")

    output_csv_file = "corrected_sentences.csv"
    with open(output_csv_file, "w", newline='', encoding='utf-8') as csvfile:
        # Define the CSV writer
        csvwriter = csv.writer(csvfile)
        
        # Write the header row
        #csvwriter.writerow(["Incorrect Sentence", "Correct Sentence", "Output-Inbuilt", "Output-GPT", "Output-Happy", "Output-HappyBase", "Output-HappyT5"])
        csvwriter.writerow(["Incorrect Sentence", "Correct Sentence", "Output-Inbuilt", "Output-GPT", "Output-Happy", "Output-HappyBase", "Output-HappyT5", "Output-HappyC4Small", "Output-HappyWill"])
        
        # Iterate over all input sentences and their corrections
        for i in range(len(correct_answers)):
            # Extract each correction for the current sentence
            inbuilt_correction = corrected_sentences_inbuilt[i][0] if i < len(corrected_sentences_inbuilt) else ""
            gpt_correction = corrected_sentences_gpt[i][0] if i < len(corrected_sentences_gpt) else ""
            happy_correction = corrected_sentences_happy[i][0] if i < len(corrected_sentences_happy) else ""
            happybase_correction = corrected_sentences_happybase[i][0] if i < len(corrected_sentences_happybase) else ""
            happyt5_correction = corrected_sentences_happyt5[i][0] if i < len(corrected_sentences_happyt5) else ""
            happyc4small_correction = corrected_sentences_happyc4small[i][0] if i < len(corrected_sentences_happyc4small) else ""
            happywill_correction = corrected_sentences_happywill[i][0] if i < len(corrected_sentences_happywill) else ""

            # Write the row for the current sentence
            #csvwriter.writerow([incorrect_strings[i], correct_answers[i], inbuilt_correction, gpt_correction, happy_correction, happybase_correction, happyt5_correction])
            csvwriter.writerow([incorrect_strings[i], correct_answers[i], inbuilt_correction, gpt_correction, happy_correction, happybase_correction, happyt5_correction, happyc4small_correction, happywill_correction])

    print(f"Results written to {output_csv_file}")