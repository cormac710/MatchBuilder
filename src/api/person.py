from src.api.base_api import BaseApi
from flask import jsonify, request
from flask_api import status
from src.dynamo_models.person import Person


class PersonApi(BaseApi):
    endpoint = 'person/'

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
        if 'email' in query_params.keys():
            email = request.args.get('email')
            person = Person.get_by_email(email)
            return jsonify(
                Person.list_as_json(person)[0]
            )

        if 'min_age' in query_keys or 'max_age' in query_keys:
            p = Person.query_by_range(
                query_params.get('min_age', None),
                query_params.get('max_age', None)
            )
            return jsonify(
                Person.list_as_json(p)
            )
        return {'error_msg': 'Invalid request from client'}, status.HTTP_400_BAD_REQUEST

    def post(self):
        request_body = request.json
        # add in request validation etc...
        person = Person.add_item(**request_body)
        if isinstance(person, Person):
            return jsonify(
                person.as_json()
            ), status.HTTP_201_CREATED
        return person, status.HTTP_400_BAD_REQUEST
