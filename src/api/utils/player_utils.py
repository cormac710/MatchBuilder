from src.dynamo_models.player import Player


class PlayerUtils:

    @classmethod
    def single_person_search(cls, query_params):
        email = query_params.get('email')
        player = Player.get_by_email(email)
        return Player.list_as_json(player)[0]

    @classmethod
    def query_limit(cls, query_keys, query_params):
        if 'limit' in query_keys:
            if int(query_params['limit']) > 100:
                return 100
            else:
                return query_params['limit']
        return 100

    @classmethod
    def last_queried_key_if_exists(cls, queried_players):
        if queried_players.last_evaluated_key:
            return queried_players.last_evaluated_key['email']['S']
