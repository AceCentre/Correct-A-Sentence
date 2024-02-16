from happytransformer import HappyTextToText, TTSettings
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

model_path = os.path.join(application_path, 't5-small-spoken-typo-tryagain')

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize HappyTextToText
happy_tt = HappyTextToText("T5", 'willwade/t5-small-spoken-typo')
args = TTSettings(num_beams=5, min_length=1)

def correct_sentence(sentence):
    try:
        result = happy_tt.generate_text(f"grammar: {sentence}", args=args)
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
