import json

from src.dynamo_models.player import Player
from tests.api.base_test import BaseApiTest


player_API = 'player/'


class ApiPlayerTest(BaseApiTest):

    def setUp(self):
        self._setup_app()
        self.set_up_table(Player)

    def test_get_player(self):
        get_player = Player.add_item('get_player', 'get_player@email.com', 22)

        self.get_request_as_json(player_API, expected_response=400)

        # GET_players = self.get_request_as_json(player_API + f'?email={get_player.email}')
        # assert GET_players['first_name'] == 'get_player'
        # assert GET_players['email'] == 'get_player@email.com'
        # assert GET_players['age'] == 22

        get_player2 = Player.add_item('get_player2', 'get_player2@email.com', 25)
        get_player3 = Player.add_item('get_player3', 'get_player3@email.com', 27)
        # test if none returned
        self.get_request_as_json(player_API, expected_response=400)

        # assert valid query
        GET_multiple_players = self.get_request_as_json(player_API + f'?min_age=21&max_age=26')
        assert len(GET_multiple_players) == 2

        assert GET_multiple_players[0]['first_name'] == get_player.first_name
        assert GET_multiple_players[0]['age'] == get_player.age

        assert GET_multiple_players[1]['first_name'] == get_player2.first_name
        assert GET_multiple_players[1]['age'] == get_player2.age

        # assert just min age
        GET_multiple_players = self.get_request_as_json(player_API + f'?min_age=24')
        assert len(GET_multiple_players) == 2
        for player in GET_multiple_players:
            assert player['age'] >= 24

        GET_multiple_players = self.get_request_as_json(player_API + f'?min_age=25')
        assert len(GET_multiple_players) == 2
        for player in GET_multiple_players:
            assert player['age'] >= 25


        # assert just max age
        GET_multiple_players = self.get_request_as_json(player_API + f'?max_age=25')
        assert len(GET_multiple_players) == 2
        for player in GET_multiple_players:
            assert player['age'] <= 25

    def test_create_player(self):
        name = 'cormac_create'
        email = 'create@create.com'
        payload = json.dumps({'first_name': name,'email': email, 'age': 28})

        created_player = self.post_request_as_json(player_API, payload)
        assert created_player['first_name'] == name
        assert created_player['email'] == email

    def test_create_player_with_same_email_as_existing(self):
        player = Player.add_item('get_player', 'get_player@email.com', 22)
        payload = json.dumps({'first_name': player.first_name,'email': player.email, 'age': 28})

        created_player = self.post_request_as_json(player_API, payload, expected_response=400)

        assert created_player['error_code'] == 'ConditionalCheckFailedException'

    def tearDown(self):
        self.delete_table(Player)
