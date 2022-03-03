import json

from src.dynamo_models.match import Match
from src.dynamo_models.player import Player
from tests.api.base_test import BaseApiTest
from tests.constants import EMAIL_1, EMAIL_2, EMAIL_3, EMAIL_4, VENUE_CITY_PARK, VENUE_LARGE_PITCH, VENUE_SMALL_PITCH

MATCH_API = 'match/'

class ApiMatchTest(BaseApiTest):

    def setUp(self):
        self._setup_app()
        self.set_up_table(Match)
        self.set_up_table(Player)

    def test_create_match(self):
        player_1 = Player.add_item('player1', EMAIL_1, 22)
        player_2 = Player.add_item('player2', EMAIL_2, 32)
        payload = json.dumps({
            'venue': 'Galway',
            'players': [player_1.email, player_2.email]
        })

        match_created_response = self.post_request_as_json(MATCH_API, payload, expected_response=201)
        assert match_created_response['venue'] == 'Galway'

    def test_get_matches(self):
        match_one = Match.add_item(VENUE_CITY_PARK, [EMAIL_1, EMAIL_3])
        match_two = Match.add_item(VENUE_SMALL_PITCH, [EMAIL_1, EMAIL_2])
        match_three = Match.add_item(VENUE_LARGE_PITCH, [EMAIL_4, EMAIL_3])
        match_four = Match.add_item(VENUE_CITY_PARK, [EMAIL_1, EMAIL_3])

        self.get_request_as_json(MATCH_API, expected_response=400)

        match_from_POST = self.get_request_as_json(MATCH_API + '?email=NOT_EXISTS')
        assert len(match_from_POST) == 0

        match_from_POST = self.get_request_as_json(MATCH_API + f'?email={EMAIL_2}')
        assert len(match_from_POST) == 1

        match_from_POST = self.get_request_as_json(MATCH_API + f'?email={EMAIL_1}')
        assert len(match_from_POST) == 3

        match_from_POST = self.get_request_as_json(MATCH_API + f'?email={EMAIL_1}&venue={VENUE_CITY_PARK}')
        assert len(match_from_POST) == 2

        match_from_POST = self.get_request_as_json(MATCH_API + f'?email={EMAIL_1}&venue={VENUE_SMALL_PITCH}')
        assert len(match_from_POST) == 1


    def tearDown(self):
        self.delete_table(Match)
        self.delete_table(Player)
