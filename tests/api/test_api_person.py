import json

from src.dynamo_models.person import Person
from tests.api.base_test import BaseApiTest


PERSON_API = 'person/'


class ApiPersonTest(BaseApiTest):

    def setUp(self):
        self._setup_app()
        self.set_up_table(Person)

    def test_get_person(self):
        get_person = Person.add_item('get_person', 'get_person@email.com', 22)

        self.get_request_as_json(PERSON_API, expected_response=400)

        # GET_people = self.get_request_as_json(PERSON_API + f'?email={get_person.email}')
        # assert GET_people['first_name'] == 'get_person'
        # assert GET_people['email'] == 'get_person@email.com'
        # assert GET_people['age'] == 22

        get_person2 = Person.add_item('get_person2', 'get_person2@email.com', 25)
        get_person3 = Person.add_item('get_person3', 'get_person3@email.com', 27)
        # test if none returned
        self.get_request_as_json(PERSON_API, expected_response=400)

        # assert valid query
        GET_multiple_people = self.get_request_as_json(PERSON_API + f'?min_age=21&max_age=26')
        assert len(GET_multiple_people) == 2

        assert GET_multiple_people[0]['first_name'] == get_person.first_name
        assert GET_multiple_people[0]['age'] == get_person.age

        assert GET_multiple_people[1]['first_name'] == get_person2.first_name
        assert GET_multiple_people[1]['age'] == get_person2.age

        # assert just min age
        GET_multiple_people = self.get_request_as_json(PERSON_API + f'?min_age=24')
        assert len(GET_multiple_people) == 2
        for person in GET_multiple_people:
            assert person['age'] >= 24

        GET_multiple_people = self.get_request_as_json(PERSON_API + f'?min_age=25')
        assert len(GET_multiple_people) == 2
        for person in GET_multiple_people:
            assert person['age'] >= 25


        # assert just max age
        GET_multiple_people = self.get_request_as_json(PERSON_API + f'?max_age=25')
        assert len(GET_multiple_people) == 2
        for person in GET_multiple_people:
            assert person['age'] <= 25

    def test_create_person(self):
        name = 'cormac_create'
        email = 'create@create.com'
        payload = json.dumps({'first_name': name,'email': email, 'age': 28})

        created_person = self.post_request_as_json(PERSON_API, payload)
        assert created_person['first_name'] == name
        assert created_person['email'] == email

    def test_create_person_with_same_email_as_existing(self):
        person = Person.add_item('get_person', 'get_person@email.com', 22)
        payload = json.dumps({'first_name': person.first_name,'email': person.email, 'age': 28})

        created_person = self.post_request_as_json(PERSON_API, payload, expected_response=400)

        assert created_person['error_code'] == 'ConditionalCheckFailedException'

    def tearDown(self):
        self.delete_table(Person)
