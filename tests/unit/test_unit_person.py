from src.dynamo_models.person import Person
from tests.api.base_test import BaseTest


class TestPerson(BaseTest):

    def setUp(self):
        self.set_up_table(Person)

    def test_crud_person(self):
        # create new item
        person_one = Person.add_item('cormac', 'c@c.c', 33)

        # retrieve from DB
        person_from_db = Person.get(person_one.email)
        assert person_from_db.first_name == 'cormac'
        assert person_from_db.email == 'c@c.c'
        assert person_from_db.age == 33

        # update
        person_from_db.update(first_name='new name')
        person_from_db_after_update = Person.get(person_one.email)
        assert person_from_db_after_update.first_name == 'new name'

        # delete
        person_from_db_after_update.delete()
        person_from_db_after_delete = person_one.scan()
        print(person_from_db_after_delete)
        assert person_from_db_after_delete.total_count == 0

    def test_create_person_already_exists(self):
        email = 'c@c.c'
        Person.add_item('cormac', email, 33)
        person_exists = Person.add_item('cormac', email, 33)
        assert person_exists['error'] == f'Person most likely already exists with email: {email}'

    def test_person_with_skills(self):
        skills_schema = {
            'passing': 10,
        }
        first_name = 'cormac'
        email = 'cormac@email.com'
        age = 25
        # create player with no skills
        person_no_skills = Person.add_item(first_name, email, age)
        assert person_no_skills.skills.passing == 0
        assert person_no_skills.skills.shooting == 0
        assert person_no_skills.skills.defending == 0
        assert person_no_skills.skills.goalkeeping == 0
        assert person_no_skills.skills.speed == 0

        person_with_one_skill = Person.add_item(first_name, 'pat@email.com', age, skills=skills_schema)
        assert person_with_one_skill.skills.passing == 10

        skills_schema['shooting'] = 5
        skills_schema['defending'] = 7
        person_with_multiple_skill = Person.add_item(first_name, 'pats@email.com', age, skills=skills_schema)
        assert person_with_multiple_skill.skills.passing == 10
        assert person_with_multiple_skill.skills.shooting == 5
        assert person_with_multiple_skill.skills.defending == 7

    def tearDown(self):
        self.delete_table(Person)
