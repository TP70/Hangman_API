import uuid
from bson import json_util
from hangman_app.models.hangman import hangman_model


class HangmanService:
    """
    Service class for managing Hangman game-related operations.

    This class provides methods for starting new games, getting game status,
    making guesses, and ending games.

    Methods:
        start_new_game(hangman_collection): Start a new Hangman game and return the game ID.
        get_all_game_status(hangman_collection): Get the status of all Hangman games.
        get_game_status(hangman_collection, game_id): Get the status of a specific Hangman game.
        make_guess(hangman_collection, game_id, data): Make a guess in a Hangman game.
        end_game(hangman_collection, game_id): End a Hangman game.
    """

    @staticmethod
    def start_new_game(hangman_collection):
        """
        Start a new Hangman game and return the game ID.

        :param hangman_collection: The MongoDB collection for Hangman games.
        :return: The game ID of the newly started game.
        """
        game_id = str(uuid.uuid4())
        word = "example"  # Replace with logic to get a random word
        new_game = {
            'game_id': game_id,
            'word': word,
            'display_word': ['_'] * len(word),
            'correct_guesses': [],
            'incorrect_guesses': [],
            'game_over': False
        }
        hangman_collection.insert_one(new_game)
        return game_id

    @staticmethod
    def get_all_game_status(hangman_collection):
        """
        Get the status of all Hangman games.

        :param hangman_collection: The MongoDB collection for Hangman games.
        :return: A list of Hangman game status.
        """
        games = list(hangman_collection.find({}, {'_id': 0}))
        return games

    @staticmethod
    def get_game_status(hangman_collection, game_id):
        """
        Get the status of a specific Hangman game.

        :param hangman_collection: The MongoDB collection for Hangman games.
        :param game_id: The ID of the Hangman game to retrieve.
        :return: The status of the Hangman game or None if not found.
        """
        game = hangman_collection.find_one({'game_id': game_id}, {'_id': 0})
        return game

    @staticmethod
    def make_guess(hangman_collection, game_id, data):
        """
        Make a guess in a Hangman game.

        :param hangman_collection: The MongoDB collection for Hangman games.
        :param game_id: The ID of the Hangman game to make a guess.
        :param data: The data containing the guessed letter.
        :return: The result of the guess.
        """
        game = hangman_collection.find_one({'game_id': game_id})
        if not game or game['game_over']:
            return {'error': 'Game not found or already over'}, 404

        letter = data.get('letter')
        if not letter or not letter.isalpha() or len(letter) != 1:
            return {'error': 'Invalid guess, please provide a single letter'}, 400

        letter = letter.lower()
        if letter in game['correct_guesses'] or letter in game['incorrect_guesses']:
            return {'error': f'You already guessed the letter {letter}'}, 400

        if letter in game['word']:
            game['correct_guesses'].append(letter)
            for i, char in enumerate(game['word']):
                if char == letter:
                    game['display_word'][i] = letter

            if all(char.isalpha() for char in game['display_word']):
                game['game_over'] = True
                return {'message': 'Congratulations! You guessed the word.', 'game': game}

        else:
            game['incorrect_guesses'].append(letter)
            if len(game['incorrect_guesses']) >= 6:
                game['game_over'] = True
                return {'message': 'Game over! You reached the maximum incorrect guesses.',
                        'game': game}

        hangman_collection.update_one({'game_id': game_id}, {'$set': game})
        return {'message': 'Guess processed successfully', 'game': game}

    @staticmethod
    def end_game(hangman_collection, game_id):
        """
        End a Hangman game.

        :param hangman_collection: The MongoDB collection for Hangman games.
        :param game_id: The ID of the Hangman game to end.
        :return: A JSON response indicating the success of the operation or a "not found" message.
        """
        result = hangman_collection.delete_one({'game_id': game_id})
        if result.deleted_count == 1:
            return {'message': 'Hangman game deleted successfully'}
        return {'error': 'Hangman game not found'}, 404
