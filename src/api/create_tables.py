from src.dynamo_models.match import Match
from src.dynamo_models.person import Person

def create_tables():
    print('INFO: Creating tables')
    if not Person.exists():
        print('Creating Person')
        Person.create_table()
        print('Person created')
    if not Match.exists():
        Match.create_table()
