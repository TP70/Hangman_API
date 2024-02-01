import uuid
import pytest

from hangman_app import create_app
from config.config import TestingConfig


class TestHangmanAPIController:
    """
    Test class for the Hangman API services.
    """

    @classmethod
    def setup_class(cls):
        cls.app = create_app(TestingConfig)
        cls.app.testing = True
        cls.client = cls.app.test_client()

    def test_start_new_game(self, mocker):
        """
        Test starting a new Hangman game via the /new_game endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("hangman_app.controllers.hangman_controller.mongo")
        # Mock the database insertion
        mongo_mock.db.hangman.insert_one.return_value.acknowledged = True

        response = self.client.post("/games")
        assert response.status_code == 200

    def test_make_guess(self, mocker):
        """
        Test making a guess in a Hangman game via the /guess/<game_id> endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("hangman_app.controllers.hangman_controller.mongo")

        # Add a Hangman game to the database with a known ID
        known_id = str(uuid.uuid4())
        mongo_mock.db.hangman.find_one.return_value = {
            "game_id": known_id,
            "word": "example",
            "display_word": ["_", "_", "_", "_", "_", "_", "_", "_"],
            "correct_guesses": [],
            "incorrect_guesses": [],
            "game_over": False,
        }

        # Mock the database update for a guess in the known game
        mongo_mock.db.hangman.update_one.return_value.modified_count = 1

        data = {"letter": "e"}

        response = self.client.post(f"/games/{known_id}", json=data)
        assert response.status_code == 200

    def test_end_game(self, mocker):
        """
        Test ending a Hangman game via the /end_game/<game_id> endpoint.

        :param mocker: Pytest mocker for mocking dependencies.
        """
        # Mock the PyMongo database object
        mongo_mock = mocker.patch("hangman_app.controllers.hangman_controller.mongo")

        # Add a Hangman game to the database with a known ID
        known_id = str(uuid.uuid4())
        mongo_mock.db.hangman.find_one.return_value = {
            "game_id": known_id,
            "word": "example",
            "display_word": ["_", "_", "_", "_", "_", "_", "_", "_"],
            "correct_guesses": [],
            "incorrect_guesses": [],
            "game_over": False,
        }

        # Mock the database deletion for the known game
        mongo_mock.db.hangman.delete_one.return_value.deleted_count = 1

        response = self.client.delete(f"/games/{known_id}")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
