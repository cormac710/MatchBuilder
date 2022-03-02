import uuid

from pynamodb import attributes
from pynamodb.exceptions import PutError

from src.dynamo_models.common_model import CommonModel
from src.dynamo_models.common_meta import CommonMeta


class Skills(attributes.MapAttribute):
    # Skills will be a rating from 1 to 10
    shooting = attributes.NumberAttribute(default=0)
    passing = attributes.NumberAttribute(default=0)
    speed = attributes.NumberAttribute(default=0)
    defending = attributes.NumberAttribute(default=0)
    goalkeeping = attributes.NumberAttribute(default=0)

    @staticmethod
    def generate_skills(shooting=None, passing=None, speed=None, defending=None, goalkeeping=None):
        skills = Skills(
            shooting=int(shooting) if shooting is not None else 0,
            passing=int(passing) if passing is not None else 0,
            speed=int(speed) if speed is not None else 0,
            defending=int(defending) if defending is not None else 0,
            goalkeeping=int(goalkeeping) if goalkeeping is not None else 0
        )
        return skills

    def as_json(self):
        return self.__dict__['attribute_values']

    @classmethod
    def list_as_json(cls, items_itr):
        return [item.as_json() for item in items_itr]


class Person(CommonModel):

    class Meta(CommonMeta):
        table_name = 'person'
    # for auth: https://dev.to/paurakhsharma/flask-rest-api-part-3-authentication-and-authorization-5935
    id = attributes.UnicodeAttribute()
    email = attributes.UnicodeAttribute(hash_key=True)
    first_name = attributes.UnicodeAttribute()
    last_name = attributes.UnicodeAttribute(null=True)
    age = attributes.NumberAttribute(null=True)
    skills = Skills(default={})

    @staticmethod
    def add_item(first_name, email, age, last_name=None, skills=None):
        # TODO check required params passed, if not throw exception
        condition = None
        condition &= Person.email != email
        skills = Skills.generate_skills(**skills) if skills is not None else {}
        person = Person(
            id=str(uuid.uuid4()),
            email=email,
            first_name=first_name,
            last_name=last_name,
            age=age,
            skills=skills
        )

        try:
            person.save(condition=condition)
            return person
        except PutError as insert_error:
            # TODO need to update to send message if email exists -> do look up and ammend message
            # TODO could not save Person -> {...}
            return {'error': insert_error.cause_response_message, 'error_code': insert_error.cause_response_code}

    @classmethod
    def get_by_email(cls, email):
        return Person.query(hash_key=email)

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save()

    @classmethod
    def query_by_range(cls, min_age=None, max_age=None):
        condition = None
        if min_age:
            condition &= Person.age >= int(min_age)
        if max_age:
            condition &= Person.age <= int(max_age)
        # User.scan(rate_limit=5)
        return Person.scan(filter_condition=condition)

    def as_json(self):
        person = super(Person, self).as_json()
        if isinstance(person['skills'], Skills):
            person['skills'] = person['skills'].as_json()
        return person

    @classmethod
    def list_as_json(cls, items_itr):
        people = super(Person, cls).list_as_json(items_itr)
        for person in people:
            if isinstance(person['skills'], Skills):
                person['skills'] = person['skills'].as_json()
        return people
