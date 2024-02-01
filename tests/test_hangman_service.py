import json
import uuid
from unittest import mock

import pytest
from hangman_app.services.hangman_service import HangmanService


class TestHangmanAPIServices:
    """
    Test class for the Hangman API services.
    """

    def test_get_game_status(self, mocker):
        """
        Test retrieving a Hangman game by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the hangman collection
        hangman_collection = mocker.MagicMock()
        # Mock the expected Hangman game
        expected_game = {
            "game_id": "game_id_1",
            "word": "example",
            "display_word": ["_", "_", "_", "_", "_", "_", "_", "_"],
            "correct_guesses": [],
            "incorrect_guesses": [],
            "game_over": False,
        }

        # Mock the find_one method
        hangman_collection.find_one.return_value = expected_game
        game_id = str(uuid.uuid4())

        game = HangmanService.get_game_status(hangman_collection, game_id)

        assert game == expected_game

    def test_get_game_status_not_found(self, mocker):
        """
        Test retrieving a non-existent Hangman game by ID.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the hangman collection
        hangman_collection = mocker.MagicMock()
        # Mock the find_one method returning None
        hangman_collection.find_one.return_value = None
        game_id = str(uuid.uuid4())

        game = HangmanService.get_game_status(hangman_collection, game_id)

        assert game is None

    def test_start_new_game(self, mocker):
        """
        Test starting a new Hangman game.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the hangman collection
        hangman_collection = mocker.MagicMock()

        # Mock the insert_one method
        hangman_collection.insert_one.return_value.acknowledged = True

        result = HangmanService.start_new_game(hangman_collection)

        assert result == mock.ANY

    def test_make_guess(self, mocker):
        """
        Test making a guess in a Hangman game.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the hangman collection
        hangman_collection = mocker.MagicMock()

        # Add a Hangman game to the database with a known ID
        known_id = str(uuid.uuid4())
        existing_game = {
            "game_id": known_id,
            "word": "example",
            "display_word": ["_", "_", "_", "_", "_", "_", "_", "_"],
            "correct_guesses": [],
            "incorrect_guesses": [],
            "game_over": False,
        }
        # Mock the find_one method
        hangman_collection.find_one.return_value = existing_game

        # Mock the database update for a guess in the known game
        hangman_collection.update_one.return_value.modified_count = 1

        data = {"letter": "e"}

        result = HangmanService.make_guess(hangman_collection, known_id, data)
        assert result == {'message': 'Guess processed successfully',
                          'game': {
                              'game_id': mock.ANY,
                              'word': 'example', 'display_word': [
                                  'e',
                                  '_',
                                  '_',
                                  '_',
                                  '_',
                                  '_',
                                  'e',
                                  '_'
                              ],
                              'correct_guesses': ['e'],
                              'incorrect_guesses': [],
                              'game_over': False}}

    def test_end_game(self, mocker):
        """
        Test ending a Hangman game.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the hangman collection
        hangman_collection = mocker.MagicMock()

        # Add a Hangman game to the database with a known ID
        known_id = str(uuid.uuid4())
        existing_game = {
            "game_id": known_id,
            "word": "example",
            "display_word": ["_", "_", "_", "_", "_", "_", "_", "_"],
            "correct_guesses": [],
            "incorrect_guesses": [],
            "game_over": False,
        }
        # Mock the find_one method
        hangman_collection.find_one.return_value = existing_game

        # Mock the database deletion for the known game
        hangman_collection.delete_one.return_value.deleted_count = 1

        result = HangmanService.end_game(hangman_collection, known_id)
        assert result == {'message': 'Hangman game deleted successfully'}


if __name__ == "__main__":
    pytest.main()
