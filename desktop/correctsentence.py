from transformers import T5Tokenizer, T5ForConditionalGeneration
import win32pipe, win32file, pywintypes, logging
import sys
import os

"""
Initializes the path to the application directory and T5 model file based on whether the app is 
running as a frozen bundle or normally. Also initializes logging.

"""
if getattr(sys, 'frozen', False):
    # If the application is running as a PyInstaller bundle
    application_path = sys._MEIPASS
else:
    # If the application is running in a normal Python environment
    application_path = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(application_path, 't5-small-spoken-typo')

# Initialize loggingIlikecheeese
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize HappyTextToText
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

def correct_sentence(sentence):
    try:
    
    # Prepare the input text with the "grammar: " prefix
        input_text = "grammar: "+sentence
        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        
        # Generate text
        # Adjust num_beams and min_length to your needs
        output = model.generate(input_ids, num_beams=5, min_length=1, max_new_tokens=50, early_stopping=True)
        
        # Decode the generated text
        decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

        result = decoded_output
        
        return result.text
    except Exception as e:
        logging.error(f"Error correcting sentence: {e}")
        return sentence  # Return the original sentence in case of error

"""
pipe_server creates a named pipe server that listens for sentences from a client.
It corrects any sentences received using the correct_sentence function, 
and sends the corrected sentence back to the client.

The server runs in an infinite loop, creating a new named pipe and waiting for a 
client connection each time. It reads sentences from the client, corrects them,
and writes the corrected sentences back over the pipe.

If any errors occur in communication over the pipe, they are logged and the server
goes back to creating a new pipe and waiting for the next client connection.
"""
def pipe_server():
    pipe_name = r'\\.\pipe\SentenceCorrectorPipe'
    logging.info("Pipe Server: Creating named pipe...")
    while True:
        try:
            pipe = win32pipe.CreateNamedPipe(
                pipe_name,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1, 65536, 65536,
                0,
                None)
            logging.info("Pipe Server: Waiting for client...")
            win32pipe.ConnectNamedPipe(pipe, None)
            logging.info("Pipe Server: Client connected.")
        except pywintypes.error as e:
            logging.error(f"Failed to create or connect named pipe: {e}")
            continue  # Attempt to create a new pipe and wait for a new connection

        try:
            while True:
                # Read the sentence from the client
                result, data = win32file.ReadFile(pipe, 64*1024)
                if result == 0:  # Check if the read was successful
                    sentence = data.decode()
                    corrected_sentence = correct_sentence(sentence)
                    win32file.WriteFile(pipe, corrected_sentence.encode())
                else:
                    break  # Break out of the inner loop if reading fails
        except pywintypes.error as e:
            logging.error(f"Communication error: {e}")
        finally:
            win32file.CloseHandle(pipe)
            logging.info("Client disconnected. Waiting for new connection...")


if __name__ == '__main__':
    pipe_server()
