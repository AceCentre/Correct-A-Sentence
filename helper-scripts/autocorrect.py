from pynput import keyboard, mouse
from pynput.keyboard import Key, Controller as KeyboardController
import requests
import clipman

clipman.init()
keyboard_controller = KeyboardController()
text_buffer = []

def correct_text(text):
    api_url = "https://api.openai.com/v1/chat/completions"
    api_key = "somekeyhere"  # Replace with your actual API key
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "Autocorrect sentence that may have typos in it and capitalization errors as well as bad spacing between words. You will not be verbose. Just return the corrected text if it can be"
            },
            {
                "role": "user",
                "content": text
            }
        ]
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        assistant_response = response.json()['choices'][0]['message']['content'].strip()
        clipman.set(assistant_response)  # Copy corrected text to clipboard
        replace_text(len(text))
    else:
        print(f"Failed to correct text. HTTP Status Code: {response.status_code}")
        print(response.text)

def replace_text(length_of_text):
    # Simulate Shift + Left Arrow to select the text
    with keyboard_controller.pressed(Key.shift):
        for _ in range(length_of_text):
            keyboard_controller.press(Key.left)
            keyboard_controller.release(Key.left)
    
    # Simulate Ctrl+V to paste the corrected text
    print('trying to now paste')
    clipman.paste()

def on_press(key):
    try:
        # Attempt to capture printable characters
        if hasattr(key, 'char') and key.char is not None:
            text_buffer.append(key.char)
        elif key == keyboard.Key.space:
            # Process text upon pressing space, for simplicity
            sentence = ''.join(text_buffer)
            if sentence.endswith('.'):
                correct_text(sentence)
                text_buffer.clear()  # Clear the buffer after processing
    except Exception as e:
        print(f"Error processing key press: {e}")


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
