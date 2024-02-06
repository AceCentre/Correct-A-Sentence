from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import logging
import wordsegment
from spellchecker import SpellChecker
import re
import json
from transformers import T5ForConditionalGeneration, T5Tokenizer
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app, version='1.0', title='Sentence Correction API', description='An API for correcting and segmenting sentences')
ns = api.namespace('correction', description='Sentence Corrections')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Define the API model
sentence_model = api.model('Sentence', {
    'text': fields.String(required=True, description='The sentence to be corrected'),
    'correct_typos': fields.Boolean(required=False, default=True, description='Whether to correct typos'),
    'correction_method': fields.String(required=False, description='Correction method: "gpt", "inbuilt", or "t5small"', enum=['gpt', 'inbuilt', 't5small'])
})

# Load necessary data for wordsegment
wordsegment.load()
# Load the modified unigrams and bigrams
with open('modified_unigrams.json', 'r') as f:
    wordsegment.UNIGRAMS = json.load(f)
with open('modified_bigrams.json', 'r') as f:
    wordsegment.BIGRAMS = json.load(f)


def download_and_save_model(model_name='willwade/t5-small-spoken-typo', model_dir='./model'):
    """
    Downloads and caches the model and tokenizer, loading them from the cache if already downloaded.
    
    Args:
    model_name (str): The name of the model on Hugging Face's model hub.
    model_dir (str): The directory where the model and tokenizer should be saved.
    """
    # Ensure the cache directory exists
    os.makedirs(model_dir, exist_ok=True)

    # Download and cache the model and tokenizer, or load from local cache if already present
    print("Checking for model and tokenizer in cache or downloading...")
    model = T5ForConditionalGeneration.from_pretrained(model_name, cache_dir=model_dir)
    tokenizer = T5Tokenizer.from_pretrained(model_name, cache_dir=model_dir)

    print("Model and tokenizer are ready.")
    return model, tokenizer
    
def setup_openAI():
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),  
        api_version="2023-12-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    return client

def correct_with_gpt(client,input_string):
    try:
        response = client.chat.completions.create(model="correctasentence", 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that corrects sentences with typos or spacing issues."},
            {"role": "user", "content": input_string},
        ])
        # Assuming the structure of the response to access the corrected text
        corrected_text = response.choices[0].message.content.strip()
        return corrected_text
    except Exception as e:
        print(f"Error in correct_with_gpt: {e}")


def create_corrector_pipeline(model_dir):
    global corrector, tokenizer, model
    print("Initializing the correction pipeline...")
    model = T5ForConditionalGeneration.from_pretrained(model_dir)
    tokenizer = T5Tokenizer.from_pretrained(model_dir)
    corrector = pipeline('text-generation', model=model, tokenizer=tokenizer)
    print("Pipeline ready.")

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app, version='1.0', title='Sentence Correction API',
          description='An API for correcting and segmenting sentences')

ns = api.namespace('correction', description='Sentence Corrections')


# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load necessary data for wordsegment
wordsegment.load()

# Load the modified unigrams and bigrams
with open('modified_unigrams.json', 'r') as f:
    wordsegment.UNIGRAMS = json.load(f)
with open('modified_bigrams.json', 'r') as f:
    wordsegment.BIGRAMS = json.load(f)

# Define the API model
sentence_model = api.model('Sentence', {
    'text': fields.String(required=True, description='The sentence to be corrected'),
    'correct_typos': fields.Boolean(required=False, default=True, description='Whether to correct typos'),
    'correction_method': fields.String(required=False, description='Correction method: "gpt", "inbuilt", or "t5small"', enum=['gpt', 'inbuilt', 't5small'])
})

# Define the main functionality
def correct_sentence(input_string, correct_typos=True):
    try:
        # Segment the string into words
        segmented = wordsegment.segment(input_string)

        # Initialize spell checker
        spell = SpellChecker()

        # Correct typos in each word if correct_typos is True
        corrected_words = [spell.correction(word) if correct_typos else word for word in segmented if word is not None]

        # Case correction (basic)
        corrected_case = []
        for word in corrected_words:
            logger.debug(f"Processing word: {word}")
            if word is not None and (re.match(r'^i\b', word) or word in ['i']):
                corrected_case.append(word.capitalize())
            else:
                corrected_case.append(word.lower() if word is not None else '')

        # Join the words into a sentence
        return ' '.join(corrected_case)
    except Exception as e:
        logger.error(f"Error in correct_sentence: {e}", exc_info=True)
        raise

        

# Define the API endpoint
@ns.route('/correct_sentence')
class SentenceCorrection(Resource):
    @api.expect(sentence_model)
    def post(self):
        try:
            data = api.payload
            input_string = data['text']
            correction_method = data.get('correction_method', 'inbuilt').lower()

            # Assuming correct_with_distilgpt2 is your method for correction
            if correction_method == 't5small':
                corrected_sentence = correct_with_t5small(input_string)
            elif correction_method == 'gpt':
                # Your GPT correction logic here
                corrected_sentence = correct_with_gpt(client,input_string)
            else:
                # Your inbuilt method logic here
                corrected_sentence = correct_sentence(input_string)

            # Make sure to return a dictionary
            return {'corrected_sentence': corrected_sentence}, 200
        except Exception as e:
            logger.error(f"Error in POST request: {e}", exc_info=True)
            return {'error': str(e)}, 500


def correct_with_t5small(input_sentence):
    global tokenizer, model  # Ensuring we are using the global variables
    
    input_ids = tokenizer.encode(input_sentence, return_tensors="pt")
    
    # Generate the corrected sentence
    output_ids = model.generate(input_ids, max_length=512)
    corrected_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return corrected_text


# Custom error handler
@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logger.exception(message)

    if not app.config.get("DEBUG"):
        return {'message': message}, 500

if __name__ == '__main__':
    # Initialize T5 model and tokenizer
    model, tokenizer = download_and_save_model(model_name='willwade/t5-small-spoken-typo', model_dir='./model')
    client = setup_openAI()
    app.run()
