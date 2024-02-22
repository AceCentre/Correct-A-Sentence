import csv
from happytransformer import HappyTextToText, TTSettings

happy_tt = HappyTextToText("T5", "willwade/5-small-spoken-typo")

args = TTSettings(num_beams=5, min_length=1)
result = happy_tt.generate_text(f"grammar: helomyfriend", args=args)
print(result.text)

table_data = []
with open("examplestrings.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Capture the header row separately
    for row in reader:
        input_sentence = row[0]  # Get the sentence from the first column
        result = happy_tt.generate_text(f"grammar: {input_sentence}", args=args)
        corrected_sentence = result.text
        table_row = [input_sentence, corrected_sentence]
        table_data.append(table_row)

width = len("Original") + 1
for row in table_data:
    print(f"Original: {row[0]:<{width}} => {row[1]}")

import pandas as pd

table_df = pd.DataFrame(table_data, columns=["Input", "Output"])
table_md = table_df.to_markdown()

with open("example_strings_table.md", "w") as md_file:
    md_file.write(table_md)