import csv
from happytransformer import HappyTextToText, TTSettings

happy_tt = HappyTextToText("T5", "willwade/t5-small-spoken-typo")

args = TTSettings(num_beams=5, min_length=1)
result = happy_tt.generate_text(f"grammar: Ireallyalikemymonkey", args=args)
print(result.text)

with open("examplestrings.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        input_sentence = row[0]  # Get the sentence from the first column
        print(f"Original: {input_sentence}")
        result = happy_tt.generate_text(f"grammar: {input_sentence}", args=args)
        corrected_sentence = result.text
        print(f"Corrected: {corrected_sentence}")
