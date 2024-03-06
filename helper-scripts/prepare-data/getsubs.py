import re
import csv
from opensubtitlescom import OpenSubtitles


# Function to extract dialogue from each subtitle entry (assuming SRT format)
def extract_dialogue_from_subtitle(subtitle_entry):
  # Access the content attribute of the Subtitle object
  content = subtitle_entry.content
  try:
    # Attempt to split with max 2 parts, handling potential exceptions
    start, end, dialogue = content.split('\n', maxsplit=2)
  except ValueError:  # If there are not enough parts, use empty strings
    try:
      # If there's only one line, use it as dialogue (assuming no time info)
      dialogue = content.strip()
    except AttributeError:  # Handle potential AttributeError for some content types
      dialogue = ''
  # Remove any leading/trailing whitespace from the dialogue
  dialogue = dialogue.strip()

  # Remove dashes at the beginning of lines using regular expressions
  dialogue = re.sub(r"^-", "", dialogue, flags=re.MULTILINE)  # Multiline flag for all lines

  # Remove HTML tags using regular expressions
  dialogue = re.sub(r"<[^>]*>", "", dialogue)  # Matches any HTML tag

  return dialogue


# Initialize the OpenSubtitles client
subtitles = OpenSubtitles(api_key="XMoMj25tyb4h2fCeDfkYpX1heCv2B5HT", user_agent="wwtrain")

# Log in (retrieve auth token)
subtitles.login(username="willwade", password="kIhvob-1hizfy-zikxax")

# Search term (replace with your desired search query)
search_term = "one day"

# Open the CSV file for writing in append mode
with open('dialogue_sentences.csv', 'a', newline='') as csvfile:
  # Create a CSV writer object
  writer = csv.writer(csvfile)

  # Iterate through all responses (page by page)
  page = 1
  while True:
    # Search for subtitles with pagination (replace with desired language)
    response = subtitles.search(query=search_term, languages="en", page=page)

    # Check if there are no more results
    if not response.data:
      break

    # Process each response (subtitle details)
    for first_subtitle in response.data:
      # Download and parse the subtitle
      srt_content = subtitles.download_and_parse(first_subtitle)

      # List to store cleaned dialogue sentences for this response
      dialogue_sentences = []

      # Iterate through each subtitle entry
      for subtitle_entry in srt_content:
        # Extract dialogue using the function
        dialogue = extract_dialogue_from_subtitle(subtitle_entry)

        # Skip empty lines before appending
        if dialogue.strip():
          dialogue_sentences.append(dialogue)

      # Write the extracted dialogue sentences to CSV
      try:
        writer.writerows(dialogue_sentences)
      except csv.Error as e:
        print(f"Error writing to CSV: {e}")



# This code will iterate through all subtitle responses for the search term,
# clean the dialogue sentences, and save them to the 'dialogue_sentences.csv' file
