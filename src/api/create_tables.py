from src.dynamo_models.match import Match
from src.dynamo_models.player import Player


def create_tables():
    print('INFO: Creating tables')
    if not Player.exists():
        print('Creating player')
        Player.create_table()
        print('player created')
    if not Match.exists():
        Match.create_table()
