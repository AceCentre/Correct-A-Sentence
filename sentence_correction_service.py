from flask import Flask, request
from flask_restx import Api, Resource, fields
from wordsegment import load, segment
from spellchecker import SpellChecker
import re

# Load necessary data for wordsegment
load()

app = Flask(__name__)
api = Api(app, version='1.0', title='Sentence Correction API',
          description='An API for correcting and segmenting sentences')

ns = api.namespace('correction', description='Sentence Corrections')

sentence_model = api.model('Sentence', {
    'text': fields.String(required=True, description='The sentence to be corrected'),
    'correct_typos': fields.Boolean(required=False, default=True, description='Whether to correct typos')
})

def correct_sentence(input_string, correct_typos=True):
    # Segment the string into words
    segmented = segment(input_string)

    # Initialize spell checker
    spell = SpellChecker()

    # Correct typos in each word if correct_typos is True
    corrected_words = [spell.correction(word) if correct_typos else word for word in segmented]

    # Case correction (basic)
    corrected_case = []
    for word in corrected_words:
        if re.match(r'^i\b', word) or word in ['i']:
            corrected_case.append(word.capitalize())
        else:
            corrected_case.append(word.lower())

    # Join the words into a sentence
    return ' '.join(corrected_case)

@ns.route('/correct_sentence')
class SentenceCorrection(Resource):
    @api.expect(sentence_model)
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        '''Correct and segment a sentence'''
        data = request.json
        input_string = data.get('text', '')
        correct_typos = data.get('correct_typos', True)
        corrected_sentence = correct_sentence(input_string, correct_typos)
        return {'corrected_sentence': corrected_sentence}

if __name__ == '__main__':
    app.run(port=80, debug=False)
