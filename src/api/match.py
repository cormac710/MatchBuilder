from src.api.base_api import BaseApi
from flask import jsonify, request
from flask_api import status
from src.dynamo_models.match import Match


class MatchApi(BaseApi):
    endpoint = 'match/'
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
        query_params = request.args
        query_keys = query_params.keys()
        if 'email' in query_keys or 'venue' in query_params:
            match = Match.get_by_query(
                email=request.args.get('email', None),
                venue=request.args.get('venue', None)
            )
            return jsonify(
                Match.list_as_json(match)
            )
        return {'error_msg': 'Invalid request from client'}, status.HTTP_400_BAD_REQUEST

    def post(self):
        request_body = request.json
        # request validation here
        print(f'request.json: {request.json}')
        match = Match.add_item(**request_body)
        return jsonify(
            match.as_json()
        ), status.HTTP_201_CREATED
