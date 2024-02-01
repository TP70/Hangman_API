from bson import json_util
from flask import request, Blueprint
from flask_restx import Resource, Api
from hangman_app import mongo
from hangman_app.models.hangman import hangman_model
from hangman_app.services.hangman_service import HangmanService

api = Api(
    Blueprint('hangman', __name__),
    version='1.0',
    title='Hangman API',
    description='API for Hangman game',
    doc='/hangman_api/swagger/swagger.json',
)


@api.route('/games')
class HangmanGames(Resource):
    """
    Resource for managing Hangman games.

    This class defines endpoints for starting new games and getting the status of existing games.

    Methods:
        post(self): Start a new Hangman game.
        get(self): Get the status of all Hangman games.

    Attributes:
        api (flask_restx.Api): The REST API used for defining endpoints.
    """

    @api.doc('Start a new Hangman game')
    def post(self):
        """
        Start a new Hangman game.

        :return: A JSON response with the game ID.
        """
        game_id = HangmanService.start_new_game(mongo.db.hangman_games)
        return {'game_id': game_id}

    @api.doc('Get the status of all Hangman games')
    def get(self):
        """
        Get the status of all Hangman games.

        :return: A list of Hangman game status.
        """
        return HangmanService.get_all_game_status(mongo.db.hangman_games)


@api.route('/games/<string:game_id>')
@api.doc(params={'game_id': 'A Hangman game ID'})
class HangmanGameResource(Resource):
    """
    Resource for managing individual Hangman games.

    This class defines endpoints for getting the status of a specific game, making a guess,
    and ending a game.

    Methods:
        get(self, game_id): Get the status of a specific Hangman game.
        post(self, game_id): Make a guess in a Hangman game.
        delete(self, game_id): End a Hangman game.

    Attributes:
        api (flask_restx.Api): The REST API used for defining endpoints.
    """

    @api.doc('Get the status of a Hangman game by ID')
    def get(self, game_id):
        """
        Get the status of a specific Hangman game by ID.

        :param game_id: The ID of the Hangman game to retrieve.
        :return: The status of the Hangman game or a "not found" message.
        """
        game_status = HangmanService.get_game_status(mongo.db.hangman_games, game_id)
        if game_status:
            return game_status
        return {"message": "Hangman game not found"}, 404

    @api.doc('Make a guess in a Hangman game')
    @api.expect(hangman_model)  # Use the hangman_model for request validation
    def post(self, game_id):
        """
        Make a guess in a Hangman game.

        :param game_id: The ID of the Hangman game to make a guess.
        :return: The result of the guess or a "not found" message.
        """
        data = request.get_json()
        result = HangmanService.make_guess(mongo.db.hangman_games, game_id, data)
        return json_util.dumps(result)

    @api.doc('End a Hangman game')
    def delete(self, game_id):
        """
        End a Hangman game.

        :param game_id: The ID of the Hangman game to end.
        :return: A JSON response indicating the success of the operation or a "not found" message.
        """
        result = HangmanService.end_game(mongo.db.hangman_games, game_id)
        return json_util.dumps(result)
