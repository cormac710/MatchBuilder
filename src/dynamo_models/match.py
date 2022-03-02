import uuid

from pynamodb import attributes

from src.dynamo_models.common_meta import CommonMeta
from src.dynamo_models.common_model import CommonModel


class Match(CommonModel):

    class Meta(CommonMeta):
        table_name = 'match'

    id = attributes.UnicodeAttribute()
    hash_key = attributes.UnicodeAttribute(hash_key=True) # id + venue
    # Will be updated to have its own class
    venue = attributes.UnicodeAttribute()
    players = attributes.ListAttribute()

    @staticmethod
    def create_hash(id, venue):
        return id + '|' + venue

    @staticmethod
    def add_item(venue, players):
        id = str(uuid.uuid4())
        match = Match(
            id=id,
            hash_key=Match.create_hash(id, venue),
            venue=venue,
            players=players
        )
        match.save()
        return match

    @classmethod
    def get_by_query(cls, email=None, venue=None):
        condition = None
        if email:
            print(f'INFO: Getting all matches which contains email: {email}')
            condition &= Match.players.contains(email)
        if venue:
            condition &= Match.venue == venue

        return Match.scan(filter_condition=condition)