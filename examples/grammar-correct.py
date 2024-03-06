import csv
from happytransformer import HappyTextToText, TTSettings

# Initialize the HappyTextToText model
happy_tt = HappyTextToText("T5", "willwade/t5-small-spoken-typo")

# Settings for the text transformation
args = TTSettings(num_beams=5, min_length=1)

# Initialize an empty list to store the data
table_data = [["Original", "Grammar-Corrected"]]

# Read sentences from the text file
with open("sent_train_aac.txt", "r") as file:
    for input_sentence in file:
        input_sentence = input_sentence.strip()  # Remove any leading/trailing whitespace
        if input_sentence:  # Check if the sentence is not empty
            # Generate the grammar-corrected sentence
            result = happy_tt.generate_text(f"grammar: {input_sentence}", args=args)
            corrected_sentence = result.text
            # Append the original and corrected sentences to the list
            table_data.append([input_sentence, corrected_sentence])

# Write the data to a CSV file
with open("corrected_sentences_train.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(table_data)

print("CSV file with original and grammar-corrected sentences has been created.")
