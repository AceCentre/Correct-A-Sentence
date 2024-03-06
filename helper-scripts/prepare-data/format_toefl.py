import csv

input_file_path = 'Annotations.csv'  # Update this to the path of your new data source
output_file_path = 'spelling-mistakes/formatted_TOEFL-SPELL.dat.txt'  # The path where you want to save the formatted data

# Dictionary to hold corrections and their misspellings
corrections_dict = {}

with open(input_file_path, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        correction = row['Correction']
        misspelling = row['Misspelling']
        if correction not in corrections_dict:
            corrections_dict[correction] = set()
        corrections_dict[correction].add(misspelling)

# Write to the output file
with open(output_file_path, mode='w', encoding='utf-8') as outfile:
    for correction, misspellings in corrections_dict.items():
        outfile.write(f'${correction}\n')
        for misspelling in misspellings:
            outfile.write(f'{misspelling}\n')
