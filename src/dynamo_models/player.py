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


class Player(CommonModel):

    class Meta(CommonMeta):
        table_name = 'player'
    id = attributes.UnicodeAttribute()
    email = attributes.UnicodeAttribute(hash_key=True)
    first_name = attributes.UnicodeAttribute()
    last_name = attributes.UnicodeAttribute(null=True)
    age = attributes.NumberAttribute(null=True)
    skills = Skills(default={})

    @staticmethod
    def add_item(first_name, email, age, last_name=None, skills=None):
        # Can do validation checks here like check the name is str, email is valid email etc...
        condition = None
        condition &= Player.email != email
        skills = Skills.generate_skills(**skills) if skills is not None else {}
        player = Player(
            id=str(uuid.uuid4()),
            email=email,
            first_name=first_name,
            last_name=last_name,
            age=age,
            skills=skills
        )

        try:
            player.save(condition=condition)
            return player
        except PutError as insert_error:
            if insert_error.cause_response_message == 'The conditional request failed':
                return {'error': f'player most likely already exists with email: {email}',
                        'error_code': insert_error.cause_response_code}
            return {'error': insert_error.cause_response_message, 'error_code': insert_error.cause_response_code}

    @classmethod
    def get_by_email(cls, email):
        return Player.query(hash_key=email)

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save()

    @classmethod
    def query_by_range(cls, min_age=None, max_age=None, limit=None, lastkey=None):
        condition = None
        if min_age:
            condition &= Player.age >= int(min_age)
        if max_age:
            condition &= Player.age <= int(max_age)
        return Player.scan(filter_condition=condition, limit=int(limit) if limit else 100, last_evaluated_key=lastkey)

    def as_json(self):
        player = super(Player, self).as_json()
        if isinstance(player['skills'], Skills):
            player['skills'] = player['skills'].as_json()
        return player

    @classmethod
    def list_as_json(cls, items_itr):
        players = super(Player, cls).list_as_json(items_itr)
        for player in players:
            if isinstance(player['skills'], Skills):
                player['skills'] = player['skills'].as_json()
        return players
