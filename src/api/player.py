from src.api.base_api import BaseApi
from flask import jsonify, request
from flask_api import status

from src.api.utils.player_utils import PlayerUtils
from src.dynamo_models.player import Player


class PlayerApi(BaseApi):
    endpoint = 'player/'

    @classmethod
    def register(cls, app):
        url = cls.api + cls.endpoint
        view_func = cls.as_view(cls.endpoint)
        app.add_url_rule(url, view_func=view_func, methods=['GET', ])
        app.add_url_rule(url, view_func=view_func, methods=['POST', ])
        app.add_url_rule(url+'<_id>',
                         view_func=view_func,
                         methods=['GET', 'PUT', 'DELETE', 'POST'])

    def get(self):
        # TODO decorator to handle bad requests
        query_params = request.args
        query_keys = query_params.keys()

        # TODO do we want email (@ special char) in url?
        if 'email' in query_params.keys():
            return jsonify(
                PlayerUtils.single_person_search(query_params)
            )

        if 'min_age' in query_keys or 'max_age' in query_keys:
            query_limit = PlayerUtils.query_limit(query_keys, query_params)
            queried_players = Player.query_by_range(
                limit=query_limit,
                lastkey=query_params.get('last_key', None),
                min_age=query_params.get('min_age', None),
                max_age=query_params.get('max_age', None)
            )
            player_as_list = Player.list_as_json(queried_players)
            return jsonify(
                {
                    "players": player_as_list,
                    'len': len(player_as_list),
                    'last_key': PlayerUtils.last_queried_key_if_exists(queried_players)
                }
            )
        else:
            return {'error_msg': 'Invalid request: min_age or max_age must be in the request'}, status.HTTP_400_BAD_REQUEST

    def post(self):
        request_body = request.json
        # add in request validation etc...
        player = Player.add_item(**request_body)
        if isinstance(player, Player):
            return jsonify(
                player.as_json()
            ), status.HTTP_201_CREATED
        return player, status.HTTP_400_BAD_REQUEST
