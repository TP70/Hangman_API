from flask_restx import fields

# Define Hangman model
hangman_model = {
    'game_id': fields.String(description='Hangman game ID'),
    'word': fields.String(description='The word to guess'),
    'display_word': fields.String(description='The word with correct guesses filled'),
    'correct_guesses': fields.List(fields.String, description='List of correct guesses'),
    'incorrect_guesses': fields.List(fields.String, description='List of incorrect guesses'),
    'game_over': fields.Boolean(description='Flag indicating whether the game is over'),
}
