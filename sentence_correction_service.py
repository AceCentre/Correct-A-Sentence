from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import logging
import wordsegment
from spellchecker import SpellChecker
import re
import json


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
    'correct_typos': fields.Boolean(required=False, default=True, description='Whether to correct typos')
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
            data = request.json
            input_string = data.get('text', '')
            correct_typos = data.get('correct_typos', True)
            corrected_sentence = correct_sentence(input_string, correct_typos)
            return {'corrected_sentence': corrected_sentence}
        except Exception as e:
            logger.error(f"Error in POST request: {e}", exc_info=True)
            return jsonify(error=str(e)), 500

# Custom error handler
@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logger.exception(message)

    if not app.config.get("DEBUG"):
        return {'message': message}, 500

if __name__ == '__main__':
    app.run()
