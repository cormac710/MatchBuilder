from src.dynamo_models.match import Match
from src.dynamo_models.person import Person
from tests.api.base_test import BaseTest
from tests.constants import EMAIL_1, EMAIL_2, EMAIL_3, VENUE_CITY_PARK, VENUE_LARGE_PITCH, VENUE_SMALL_PITCH


class TestMatch(BaseTest):

    def setUp(self):
        self.set_up_table(Match)
        self.set_up_table(Person)

    def test_crud_match(self):
        cormac = Person.add_item('cormac', 'c@c.c', 34)
        john = Person.add_item('john', 'j@c.c', 43)

        # create match
        main_match = Match.add_item(VENUE_SMALL_PITCH, [cormac.email, john.email])

        # retrieve from DB
        match_from_db = Match.get(main_match.hash_key)
        assert match_from_db.venue == VENUE_SMALL_PITCH
        assert len(match_from_db.players) == 2
        assert match_from_db.players[0] == cormac.email

    def test_get_match_by_email(self):

        # create match
        Match.add_item(VENUE_CITY_PARK, [EMAIL_1, EMAIL_2])
        Match.add_item(VENUE_LARGE_PITCH, [EMAIL_1, EMAIL_3])

        match_fetched_from_db = Match.get_by_query(email='blank_email')
        assert len(list(match_fetched_from_db)) == 0

        match_fetched_from_db = Match.get_by_query(email=EMAIL_2)
        assert len(list(match_fetched_from_db)) == 1

        match_fetched_from_db = Match.get_by_query(email=EMAIL_1)
        assert len(list(match_fetched_from_db)) == 2

    def test_get_by_venue(self):
        # create match
        Match.add_item(VENUE_CITY_PARK, [EMAIL_1, EMAIL_2])
        Match.add_item(VENUE_CITY_PARK, [EMAIL_1, EMAIL_3])
        Match.add_item(VENUE_LARGE_PITCH, [EMAIL_1, EMAIL_3])

        match_fetched_from_db = Match.get_by_query(venue='blank_venue')
        assert len(list(match_fetched_from_db)) == 0

        match_fetched_from_db = Match.get_by_query(venue=VENUE_LARGE_PITCH)
        assert len(list(match_fetched_from_db)) == 1

        match_fetched_from_db = Match.get_by_query(venue=VENUE_CITY_PARK)
        assert len(list(match_fetched_from_db)) == 2

    def test_multiple_query(self):
        # create match
        Match.add_item(VENUE_CITY_PARK, [EMAIL_1, EMAIL_2])
        Match.add_item(VENUE_CITY_PARK, [EMAIL_1, EMAIL_3])
        Match.add_item(VENUE_LARGE_PITCH, [EMAIL_1, EMAIL_3])
        Match.add_item(VENUE_LARGE_PITCH, [EMAIL_2, EMAIL_3])

        match_fetched_from_db = Match.get_by_query(venue='blank_venue', email='blank_email')
        assert len(list(match_fetched_from_db)) == 0

        match_fetched_from_db = Match.get_by_query(venue=VENUE_CITY_PARK, email=EMAIL_3)
        assert len(list(match_fetched_from_db)) == 1

        match_fetched_from_db = Match.get_by_query(venue=VENUE_CITY_PARK, email=EMAIL_1)
        assert len(list(match_fetched_from_db)) == 2

        match_fetched_from_db = Match.get_by_query(venue=VENUE_LARGE_PITCH, email=EMAIL_3)
        assert len(list(match_fetched_from_db)) == 2

        match_fetched_from_db = Match.get_by_query(venue=VENUE_LARGE_PITCH, email=EMAIL_2)
        assert len(list(match_fetched_from_db)) == 1

    def tearDown(self):
        self.delete_table(Match)
        self.delete_table(Person)
