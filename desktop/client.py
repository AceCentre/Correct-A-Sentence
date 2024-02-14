import sys
import argparse
import logging
import pyperclip
import win32file
import win32pipe
import pywintypes
import time

# Setup logging
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import time

def send_to_pipe(sentence, retries=3, delay=1):
    pipe_name = r'\\.\pipe\SentenceCorrectorPipe'
    attempt = 0
    while attempt < retries:
        try:
            handle = win32file.CreateFile(
                pipe_name,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0, None,
                win32file.OPEN_EXISTING,
                0, None)
            win32file.WriteFile(handle, sentence.encode())
            result, data = win32file.ReadFile(handle, 64*1024)
            corrected_sentence = data.decode()
            win32file.CloseHandle(handle)
            return corrected_sentence
        except pywintypes.error as e:
            logging.error(f"Attempt {attempt + 1}: Error communicating with the pipe server: {e}")
            time.sleep(delay)  # Wait before retrying
            attempt += 1
    return None


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

    corrected_sentence = send_to_pipe(sentence)
    if corrected_sentence:
        if args.return_string:
            print(corrected_sentence)
        else:
            try:
                pyperclip.copy(corrected_sentence)
            except Exception as e:
                logging.error(f"Error writing to clipboard: {e}")
    else:
        logging.error("Failed to correct the sentence due to an error with the pipe server.")

if __name__ == "__main__":
    main()
