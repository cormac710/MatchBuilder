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

        GET_players = self.get_request_as_json(player_API + f'?email={get_player.email}')
        assert GET_players['first_name'] == 'get_player'
        assert GET_players['email'] == 'get_player@email.com'
        assert GET_players['age'] == 22

        get_player2 = Player.add_item('get_player2', 'get_player2@email.com', 25)
        get_player3 = Player.add_item('get_player3', 'get_player3@email.com', 27)
        # test if none returned
        self.get_request_as_json(player_API, expected_response=400)

        # assert valid query
        GET_multiple_players = self.get_request_as_json(player_API + f'?min_age=21&max_age=26')
        assert GET_multiple_players['len'] == 2

        assert GET_multiple_players['players'][0]['first_name'] == get_player.first_name
        assert GET_multiple_players['players'][0]['age'] == get_player.age

        assert GET_multiple_players['players'][1]['first_name'] == get_player2.first_name
        assert GET_multiple_players['players'][1]['age'] == get_player2.age

        # assert just min age
        GET_multiple_players = self.get_request_as_json(player_API + f'?min_age=24')
        assert len(GET_multiple_players['players']) == 2
        for player in GET_multiple_players['players']:
            assert player['age'] >= 24

        GET_multiple_players = self.get_request_as_json(player_API + f'?min_age=25')
        assert len(GET_multiple_players['players']) == 2
        for player in GET_multiple_players['players']:
            assert player['age'] >= 25

        # assert just max age
        GET_multiple_players = self.get_request_as_json(player_API + f'?max_age=25')
        assert GET_multiple_players['len'] == 2
        for player in GET_multiple_players['players']:
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

    def test_get_player_with_limits(self):
        ages = [20, 24, 28, 30, 44]
        for i in range(5):
            Player.add_item(f'player{i}', f'player{i}@email.com', ages[i])
        assert Player.count() == 5
        # invalid_request = self.get_request_as_json(player_API + '?limit=3', expected_response=400)
        # assert invalid_request['error_msg'] == 'Invalid request: min_age or max_age must be in the request'

        players_batch_1 = self.get_request_as_json(player_API + '?min_age=19&limit=3')
        key_of_last_player_returned = players_batch_1['players'][-1]['email']
        assert len(players_batch_1['players']) == 3
        # check last key is equal to the email (hash key) of the last element in the array
        assert players_batch_1['last_key'] == key_of_last_player_returned

        players_batch_2 = self.get_request_as_json(
            player_API + f'?min_age=19&limit=3&last_key={key_of_last_player_returned}')
        # only 2 players left in DB
        assert len(players_batch_2['players']) == 2
        assert players_batch_2['last_key'] == None

    def tearDown(self):
        self.delete_table(Player)
