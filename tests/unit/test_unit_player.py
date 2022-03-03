from src.dynamo_models.player import Player
from tests.api.base_test import BaseTest


class TestPlayer(BaseTest):

    def setUp(self):
        self.set_up_table(Player)

    def test_crud_player(self):
        # create new item
        player_one = Player.add_item('cormac', 'c@c.c', 33)

        # retrieve from DB
        player_from_db = Player.get(player_one.email)
        assert player_from_db.first_name == 'cormac'
        assert player_from_db.email == 'c@c.c'
        assert player_from_db.age == 33

        # update
        player_from_db.update(first_name='new name')
        player_from_db_after_update = Player.get(player_one.email)
        assert player_from_db_after_update.first_name == 'new name'

        # delete
        player_from_db_after_update.delete()
        player_from_db_after_delete = player_one.scan()
        print(player_from_db_after_delete)
        assert player_from_db_after_delete.total_count == 0

    def test_create_player_already_exists(self):
        email = 'c@c.c'
        Player.add_item('cormac', email, 33)
        player_exists = Player.add_item('cormac', email, 33)
        assert player_exists['error'] == f'player most likely already exists with email: {email}'

    def test_player_with_skills(self):
        skills_schema = {
            'passing': 10,
        }
        first_name = 'cormac'
        email = 'cormac@email.com'
        age = 25
        # create player with no skills
        player_no_skills = Player.add_item(first_name, email, age)
        assert player_no_skills.skills.passing == 0
        assert player_no_skills.skills.shooting == 0
        assert player_no_skills.skills.defending == 0
        assert player_no_skills.skills.goalkeeping == 0
        assert player_no_skills.skills.speed == 0

        player_with_one_skill = Player.add_item(first_name, 'pat@email.com', age, skills=skills_schema)
        assert player_with_one_skill.skills.passing == 10

        skills_schema['shooting'] = 5
        skills_schema['defending'] = 7
        player_with_multiple_skill = Player.add_item(first_name, 'pats@email.com', age, skills=skills_schema)
        assert player_with_multiple_skill.skills.passing == 10
        assert player_with_multiple_skill.skills.shooting == 5
        assert player_with_multiple_skill.skills.defending == 7

    def tearDown(self):
        self.delete_table(Player)
